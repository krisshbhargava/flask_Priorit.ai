using System.Diagnostics;
using System.Reflection.Metadata;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Priorit.ai.Pages;

public class PrivacyModel : PageModel
{
    private readonly ILogger<PrivacyModel> _logger;


    public PrivacyModel(ILogger<PrivacyModel> logger)
    {
        _logger = logger;
    }

    public void OnGet()
    {
    }

    public IActionResult OnPost() {
        if (!ModelState.IsValid)
        {
            // If the model state is not valid (which includes anti-forgery token validation), re-render the page
            return Page(); // This will show validation errors if any
        }

        // Extract form data
        var studentId = Request.Form["student_id"];
        var building = Request.Form["building"];
        var category = Request.Form["category"];
        var description = Request.Form["description"];
            
        // Here you can process the data or call your Python function

        _logger.LogInformation($"Student ID: {studentId}");
        _logger.LogInformation($"Building: {building}");
        _logger.LogInformation($"Category: {category}");
        _logger.LogInformation($"Description: {description}");

            
        // Return a view or redirect
        return Redirect("/Index"); // Or any other page
    }
}


