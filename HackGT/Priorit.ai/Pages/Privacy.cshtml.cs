using System.Diagnostics;
using System.Reflection.Metadata;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Priorit.ai.Pages;

public class PrivacyModel : PageModel
{
    private readonly ILogger<PrivacyModel> _logger;

    public string InputData { get; set; }

    public string Result { get; set; }

    public PrivacyModel(ILogger<PrivacyModel> logger)
    {
        _logger = logger;
    }

    public void OnGet()
    {
    }

    public IActionResult SubmitForm(string studentId, string building, string category, string description)
    {
        string userCat = category;
        string userDesc = description;
        string pythonScriptPath = "FinalModel.py";
        string[] pythonInput = new string[2];
        pythonInput[0] = userCat;
        pythonInput[1] = userDesc;

        CallPythonModel(pythonInput);

        return Redirect("https://www.cnn.com/");
    }

    private string CallPythonModel(string[] inputData)
    {
        var psi = new System.Diagnostics.ProcessStartInfo
        {
            FileName = "python", // Ensure Python is in your PATH or provide full path
            Arguments = $"your_model_script.py \"{inputData}\"",
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using (var process = Process.Start(psi))
        {
            using (var reader = process.StandardOutput)
            {
                string result = reader.ReadToEnd();
                process.WaitForExit();
                return result;
            }
        }
    }
}


