package com.heritagehub.org.Kickstart.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ApiService {

    private final RestTemplate restTemplate = new RestTemplate();

    public String sendToApi(String filePath) {
        // Make an HTTP request to your API with the file path and get the response
//        String apiResponse = restTemplate.getForObject("http://127.0.0.1:5000/processFile/" + filePath, String.class);
        String apiResponse = restTemplate.getForObject("http://127.0.0.1:5000/processFile/video.mp4", String.class);
        return apiResponse;
    }
}
