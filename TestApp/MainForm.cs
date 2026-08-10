namespace Win2APKTest;

public sealed class MainForm : Form
{
    private const string HelloText = "Hola mundo";
    private const string ChangedText = "Texto cambiado";

    private readonly Label messageLabel;
    private readonly Button toggleButton;
    private bool isTextChanged;

    public MainForm()
    {
        Text = "Win2APK Test";
        StartPosition = FormStartPosition.CenterScreen;
        ClientSize = new Size(420, 190);
        MinimumSize = new Size(360, 160);
        FormBorderStyle = FormBorderStyle.FixedSingle;
        MaximizeBox = false;

        messageLabel = new Label
        {
            AutoSize = false,
            Dock = DockStyle.Top,
            Height = 90,
            Text = HelloText,
            TextAlign = ContentAlignment.MiddleCenter,
            Font = new Font("Segoe UI", 18F, FontStyle.Regular, GraphicsUnit.Point),
        };

        toggleButton = new Button
        {
            AutoSize = true,
            Text = "Cambiar texto",
            TabIndex = 0,
            AccessibleName = "Cambiar texto",
            AccessibleDescription = "Alterna el texto de la ventana",
        };
        toggleButton.Click += ToggleButton_Click;

        var buttonPanel = new Panel
        {
            Dock = DockStyle.Fill,
        };
        buttonPanel.Controls.Add(toggleButton);
        buttonPanel.Resize += (_, _) =>
        {
            toggleButton.Left = (buttonPanel.ClientSize.Width - toggleButton.Width) / 2;
            toggleButton.Top = (buttonPanel.ClientSize.Height - toggleButton.Height) / 2;
        };

        Controls.Add(buttonPanel);
        Controls.Add(messageLabel);
    }

    private void ToggleButton_Click(object? sender, EventArgs e)
    {
        isTextChanged = !isTextChanged;
        messageLabel.Text = isTextChanged ? ChangedText : HelloText;
        Console.WriteLine($"[Win2APKTest] Botón activado. Texto actual: {messageLabel.Text}");
    }
}
