package com.topicos.movies.history.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.topicos.movies.history.exceptions.EmptyHistoryMoviesException;

import java.util.List;

public interface IMoviesService {
    void addMovieToHistory(JsonNode movie);
    List<JsonNode> getHistory() throws EmptyHistoryMoviesException;
    JsonNode getLastSavedMovie() throws EmptyHistoryMoviesException;
}
