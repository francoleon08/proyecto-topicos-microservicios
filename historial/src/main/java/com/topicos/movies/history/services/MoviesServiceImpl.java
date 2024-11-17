package com.topicos.movies.history.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.topicos.movies.history.exceptions.AlreadyExistMovieException;
import com.topicos.movies.history.exceptions.EmptyHistoryMoviesException;
import com.topicos.movies.history.repositories.MoviesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MoviesServiceImpl implements IMoviesService {

    @Autowired
    private MoviesRepository moviesRepository;

    @Override
    public void addMovieToHistory(JsonNode movie) {
        try {
            moviesRepository.addMovieToHistory(movie);
        } catch (AlreadyExistMovieException ignore) {}
    }

    @Override
    public List<JsonNode> getHistory() throws EmptyHistoryMoviesException {
        if(moviesRepository.siEmpty()) {
            throw new EmptyHistoryMoviesException("No movies in history");
        } else {
            return moviesRepository.getMovies();
        }
    }

    @Override
    public JsonNode getLastSavedMovie() throws EmptyHistoryMoviesException {
        if(moviesRepository.siEmpty()) {
            throw new EmptyHistoryMoviesException("No movies in history");
        } else {
            return moviesRepository.getLastSavedMovie();
        }
    }
}
