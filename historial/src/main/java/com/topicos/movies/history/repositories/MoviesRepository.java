package com.topicos.movies.history.repositories;

import com.fasterxml.jackson.databind.JsonNode;
import com.topicos.movies.history.exceptions.AlreadyExistMovieException;
import org.springframework.stereotype.Repository;

import java.util.LinkedList;
import java.util.List;

@Repository
public class MoviesRepository {

    private LinkedList<JsonNode> movies;

    public MoviesRepository() {
        movies = new LinkedList<JsonNode>();
    }

    public void addMovieToHistory(JsonNode movie) throws AlreadyExistMovieException {
        if (movies.contains(movie)) {
            throw new AlreadyExistMovieException("Movie already exists in history");
        }
        movies.addFirst(movie);
    }

    public boolean siEmpty() {
        return movies.isEmpty();
    }

    public List<JsonNode> getMovies() {
        return movies;
    }

    public JsonNode getLastSavedMovie() {
        return movies.getFirst();
    }
}
