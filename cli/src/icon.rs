use std::fs;
use std::path::Path;

use anyhow::{Context, Result, bail, ensure};
use image::imageops::{FilterType, overlay, resize};
use image::{GenericImageView, ImageBuffer, Rgba, RgbaImage};

use crate::paths::write_atomic;

const DENSITIES: [(&str, f32); 5] = [
    ("mdpi", 1.0),
    ("hdpi", 1.5),
    ("xhdpi", 2.0),
    ("xxhdpi", 3.0),
    ("xxxhdpi", 4.0),
];

pub fn generate(source: &Path, background: &str, output: &Path) -> Result<()> {
    if output.exists() {
        fs::remove_dir_all(output)?;
    }
    fs::create_dir_all(output)?;
    let normalized = load(source)?;
    let color = parse_color(background)?;

    write_atomic(
        &output.join("values/win2apk_launcher_background.xml"),
        format!(
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>\n    <color name=\"win2apk_launcher_background\">{background}</color>\n</resources>\n"
        )
        .as_bytes(),
    )?;

    for (density, multiplier) in DENSITIES {
        let adaptive_size = (108.0 * multiplier).round() as u32;
        let safe_size = (66.0 * multiplier).round() as u32;
        let legacy_size = (48.0 * multiplier).round() as u32;
        let directory = output.join(format!("mipmap-{density}"));
        fs::create_dir_all(&directory)?;

        let foreground = contain(&normalized, safe_size, adaptive_size);
        foreground.save(directory.join("win2apk_launcher_foreground.png"))?;

        let mut monochrome = RgbaImage::new(adaptive_size, adaptive_size);
        for (x, y, pixel) in foreground.enumerate_pixels() {
            monochrome.put_pixel(x, y, Rgba([255, 255, 255, pixel[3]]));
        }
        monochrome.save(directory.join("win2apk_launcher_monochrome.png"))?;

        let content_size = ((legacy_size as f32) * 0.9).round() as u32;
        let legacy_foreground = contain(&normalized, content_size, legacy_size);
        let mut legacy = ImageBuffer::from_pixel(legacy_size, legacy_size, color);
        overlay(&mut legacy, &legacy_foreground, 0, 0);
        legacy.save(directory.join("win2apk_launcher.png"))?;
        legacy.save(directory.join("win2apk_launcher_round.png"))?;
    }

    let adaptive = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<adaptive-icon xmlns:android=\"http://schemas.android.com/apk/res/android\">\n    <background android:drawable=\"@color/win2apk_launcher_background\" />\n    <foreground android:drawable=\"@mipmap/win2apk_launcher_foreground\" />\n    <monochrome android:drawable=\"@mipmap/win2apk_launcher_monochrome\" />\n</adaptive-icon>\n";
    write_atomic(
        &output.join("mipmap-anydpi-v26/win2apk_launcher.xml"),
        adaptive.as_bytes(),
    )?;
    write_atomic(
        &output.join("mipmap-anydpi-v26/win2apk_launcher_round.xml"),
        adaptive.as_bytes(),
    )?;
    Ok(())
}

fn load(path: &Path) -> Result<RgbaImage> {
    let image = if path
        .extension()
        .and_then(|value| value.to_str())
        .is_some_and(|value| value.eq_ignore_ascii_case("svg"))
    {
        render_svg(path)?
    } else {
        image::open(path)
            .with_context(|| format!("formato de icono no admitido: {}", path.display()))?
            .to_rgba8()
    };
    Ok(trim_transparent(image))
}

fn render_svg(path: &Path) -> Result<RgbaImage> {
    let data = fs::read(path)?;
    let options = resvg::usvg::Options::default();
    let tree = resvg::usvg::Tree::from_data(&data, &options)
        .with_context(|| format!("SVG inválido: {}", path.display()))?;
    let size = tree.size();
    let scale = (2048.0 / size.width()).min(2048.0 / size.height());
    let width = (size.width() * scale).ceil() as u32;
    let height = (size.height() * scale).ceil() as u32;
    let mut pixmap = resvg::tiny_skia::Pixmap::new(width.max(1), height.max(1))
        .context("el SVG excede el tamaño de imagen admitido")?;
    resvg::render(
        &tree,
        resvg::tiny_skia::Transform::from_scale(scale, scale),
        &mut pixmap.as_mut(),
    );
    RgbaImage::from_raw(width, height, pixmap.data().to_vec())
        .context("no se pudo convertir el SVG renderizado")
}

fn trim_transparent(image: RgbaImage) -> RgbaImage {
    let (width, height) = image.dimensions();
    let mut min_x = width;
    let mut min_y = height;
    let mut max_x = 0;
    let mut max_y = 0;
    let mut found = false;
    for (x, y, pixel) in image.enumerate_pixels() {
        if pixel[3] != 0 {
            min_x = min_x.min(x);
            min_y = min_y.min(y);
            max_x = max_x.max(x);
            max_y = max_y.max(y);
            found = true;
        }
    }
    if !found {
        return image;
    }
    image
        .view(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        .to_image()
}

fn contain(image: &RgbaImage, content_size: u32, canvas_size: u32) -> RgbaImage {
    let (width, height) = image.dimensions();
    let ratio = (content_size as f64 / width as f64).min(content_size as f64 / height as f64);
    let target_width = ((width as f64 * ratio).round() as u32).max(1);
    let target_height = ((height as f64 * ratio).round() as u32).max(1);
    let resized = resize(image, target_width, target_height, FilterType::Lanczos3);
    let mut canvas = RgbaImage::new(canvas_size, canvas_size);
    let x = (canvas_size - target_width) / 2;
    let y = (canvas_size - target_height) / 2;
    overlay(&mut canvas, &resized, x.into(), y.into());
    canvas
}

fn parse_color(value: &str) -> Result<Rgba<u8>> {
    ensure!(
        matches!(value.len(), 7 | 9) && value.starts_with('#'),
        "color inválido: {value}"
    );
    let red = u8::from_str_radix(&value[1..3], 16)?;
    let green = u8::from_str_radix(&value[3..5], 16)?;
    let blue = u8::from_str_radix(&value[5..7], 16)?;
    let alpha = if value.len() == 9 {
        u8::from_str_radix(&value[7..9], 16)?
    } else {
        255
    };
    if alpha == 0 {
        bail!("el fondo del icono no puede ser completamente transparente");
    }
    Ok(Rgba([red, green, blue, alpha]))
}
