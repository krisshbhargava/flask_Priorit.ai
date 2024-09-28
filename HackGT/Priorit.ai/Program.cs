var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseUrls("http://localhost:5111");

// Add services to the container.
builder.Services.AddRazorPages();

builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-XSRF-TOKEN"; // Optional: customize header name
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

// Define your custom endpoint for form submission
app.MapPost("/submit", async (HttpContext context, ILogger<Program> logger) =>
{
    var form = await context.Request.ReadFormAsync();
    
    var studentId = form["student_id"];
    var building = form["building"];
    var category = form["category"];
    var description = form["description"];

    // Log the form data
    logger.LogInformation($"Student ID: {studentId}");
    logger.LogInformation($"Building: {building}");
    logger.LogInformation($"Category: {category}");
    logger.LogInformation($"Description: {description}");

    // Redirect after processing the form
    context.Response.Redirect("/Index"); // Or redirect to any other page
});

// Map Razor Pages
app.MapRazorPages();

app.Run();
