package com.topicos.movies.history.services;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

@Service
public class RabbitService {

    private final RabbitTemplate rabbitTemplate;

    public RabbitService(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendMovie(String movie) {
        System.out.println(movie);
        rabbitTemplate.convertAndSend("movies", movie);
    }
}
