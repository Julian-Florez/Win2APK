using System.Runtime.InteropServices;

namespace Win2APKTest;

internal static class Program
{
    [STAThread]
    private static int Main()
    {
        Console.WriteLine("[Win2APKTest] Iniciando aplicación...");
        Console.WriteLine($"[Win2APKTest] Runtime: {RuntimeInformation.FrameworkDescription}");
        Console.WriteLine($"[Win2APKTest] Arquitectura del proceso: {RuntimeInformation.ProcessArchitecture}");
        Console.WriteLine($"[Win2APKTest] Sistema operativo: {RuntimeInformation.OSDescription}");
        Console.WriteLine($"[Win2APKTest] Directorio: {AppContext.BaseDirectory}");
        Console.WriteLine($"[Win2APKTest] PID: {Environment.ProcessId}");

        AppDomain.CurrentDomain.UnhandledException += CurrentDomain_UnhandledException;
        TaskScheduler.UnobservedTaskException += TaskScheduler_UnobservedTaskException;

        try
        {
            Application.SetUnhandledExceptionMode(UnhandledExceptionMode.CatchException);
            Application.ThreadException += Application_ThreadException;
            ApplicationConfiguration.Initialize();

            using var form = new MainForm();
            Console.WriteLine("[Win2APKTest] Ventana creada. Esperando interacción...");
            Application.Run(form);
            Console.WriteLine("[Win2APKTest] Aplicación cerrada normalmente.");
            return 0;
        }
        catch (Exception exception)
        {
            WriteException("Excepción fatal durante el inicio o ejecución", exception);
            return 1;
        }
    }

    private static void Application_ThreadException(object? sender, ThreadExceptionEventArgs e)
    {
        WriteException("Excepción en el hilo de interfaz", e.Exception);
    }

    private static void CurrentDomain_UnhandledException(object? sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception exception)
        {
            WriteException($"Excepción no controlada (terminating={e.IsTerminating})", exception);
        }
        else
        {
            Console.Error.WriteLine($"[Win2APKTest][ERROR] Excepción no controlada: {e.ExceptionObject}");
        }
    }

    private static void TaskScheduler_UnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        WriteException("Excepción no observada en una tarea", e.Exception);
        e.SetObserved();
    }

    private static void WriteException(string message, Exception exception)
    {
        Console.Error.WriteLine($"[Win2APKTest][ERROR] {message}");
        Console.Error.WriteLine(exception.ToString());
    }
}
