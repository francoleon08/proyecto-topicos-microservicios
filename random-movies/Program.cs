using DotNetEnv;
var builder = WebApplication.CreateBuilder(args);

Env.Load();

builder.Services.AddHttpClient();
builder.Services.AddControllers();

var app = builder.Build();

app.UseAuthorization();
app.MapControllers();

app.Run();
