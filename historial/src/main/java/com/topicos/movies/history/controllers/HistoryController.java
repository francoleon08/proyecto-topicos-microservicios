package com.topicos.movies.history.controllers;

import com.fasterxml.jackson.databind.JsonNode;
import com.topicos.movies.history.exceptions.EmptyHistoryMoviesException;
import com.topicos.movies.history.exceptions.NotMovieJsonException;
import com.topicos.movies.history.services.IMoviesService;
import com.topicos.movies.history.utils.JsonVerify;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;

@RestController
@RequestMapping("/history")
public class HistoryController {

    @Autowired
    private IMoviesService moviesService;

    @PostMapping
    public ResponseEntity<?> addMovieToHistory(@RequestBody JsonNode movie) {
        try {
            JsonVerify.isMoviesJson(movie);
            moviesService.addMovieToHistory(movie);
            return ResponseEntity.ok().build();
        } catch (NotMovieJsonException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("lastSaved")
    public ResponseEntity<?> getLastSavedMovie() {
        try {
            return ResponseEntity.ok(moviesService.getLastSavedMovie());
        } catch (EmptyHistoryMoviesException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("allHistory")
    public ResponseEntity<?> getAllHistory() {
        try {
            return ResponseEntity.ok(moviesService.getHistory());
        } catch (EmptyHistoryMoviesException e) {
            return ResponseEntity.ok(new ArrayList<>());
        }
    }
}
