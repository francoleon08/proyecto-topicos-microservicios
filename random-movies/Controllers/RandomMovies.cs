using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

[ApiController]
[Route("randommovies")]
public class RandomMovies : ControllerBase
{

    private readonly HttpClient _httpClient;    
    private readonly string _moviesUrl;

    public RandomMovies(HttpClient httpClient, IConfiguration configuration) {
        _httpClient = httpClient;
        _moviesUrl = configuration["URL_MOVIES"] ?? throw new System.Exception("URL_MOVIES is not set");        
    }
    
    public async Task<IActionResult> GetRandomMovies([FromQuery] int limit)
    {        
        try {                        
            checkLimit(limit);
            var response = await _httpClient.GetAsync($"{_moviesUrl}/movies/random?limit={limit}");
            
            if (!response.IsSuccessStatusCode) {
                return StatusCode((int)response.StatusCode, new { message = "Error fetching random movies" });
            }

            var jsonResponse = await response.Content.ReadAsStringAsync();
            var movies = JsonSerializer.Deserialize<object>(jsonResponse);

            return Ok(movies);
        }
        catch (System.Exception ex) {            
            return StatusCode(500, new { message = "Error fetching random movies", details = ex.Message });
        }
    }

    private void checkLimit(int limit) {
        if (limit <= 0) {
            throw new Exception("Limit must be greater than 0");
        }        
    }
}


