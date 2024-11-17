package com.topicos.movies.history.utils;

import com.fasterxml.jackson.databind.JsonNode;
import com.topicos.movies.history.exceptions.NotMovieJsonException;

public class JsonVerify {

    public static boolean isMoviesJson(JsonNode movie) throws NotMovieJsonException {
        if (movie.has("title") && movie.has("imdb")) {
            return true;
        } else {
            throw new NotMovieJsonException("The JSON is not a movie");
        }
    }
}
