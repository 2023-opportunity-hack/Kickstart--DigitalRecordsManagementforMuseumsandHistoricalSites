package com.heritagehub.org.Kickstart.service;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.heritagehub.org.Kickstart.models.HeritageDocument;
import com.heritagehub.org.Kickstart.repository.ElasticSearchQuery;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;

@Service
public class FileProcessorService {

    @Autowired
    private ApiService apiService;

    @Autowired
    private ElasticSearchQuery elasticSearchQuery;

    @Async
    @EventListener(ApplicationReadyEvent.class)
    public void processFolder() throws IOException {
//        try (Stream<Path> paths = Files.walk(Path.of("/Users/saharshgoenka/PycharmProjects/Kickstart--DigitalRecordsManagementforMuseumsandHistoricalSites/code_lib/test_files"))) {
//            paths
////                    .filter(Files::isRegularFile)
//                    .forEach(filePath -> {
//                        String filePathStr = filePath.toString();
//                        // Send the file path to the API and get the response
//                        String apiResponse = apiService.sendToApi(filePathStr);
//
//
//                        // Create a ResponseDocument and save it to Elasticsearch
//                        HeritageDocument responseDocument = new HeritageDocument();
//                    });
//        }
        try {

        String apiResponse = apiService.sendToApi("../../../PycharmProjects/Kickstart--DigitalRecordsManagementforMuseumsandHistoricalSites/tag_generator/video.mp4");
            ObjectMapper objectMapper = new ObjectMapper();

            // Parse the JSON string into a JsonNode
            JsonNode jsonNode = objectMapper.readTree(apiResponse);

            // Extract the "tags" array as a separate string array
            JsonNode tagsNode = jsonNode.get("tags");

            if (tagsNode != null && tagsNode.isArray()) {
                HeritageDocument hd = new HeritageDocument();

                String[] tagsArray = objectMapper.convertValue(tagsNode, String[].class);

                hd.setFileTags(tagsArray);
                hd.setFilePath("video.mp4");
//                // Print the tags
//                for (String tag : tagsArray) {
//                    System.out.println(tag);
//                }
                elasticSearchQuery.createOrUpdateDocument(hd);

            }
//        hd.setFilePath("testqwefqwefhme");
//        hd.setId("923875");
//            String tags[] = new String[4];
//            tags[0] = "world";
//            tags[1] = "usa";
//            tags[2] = "india";
//            tags[3] = "meta";
//            hd.setFileTags(tags);
//        elasticSearchQuery.createOrUpdateDocument(hd);
//            hd = new HeritageDocument();
//            String tags1[] = new String[1];
//            tags1[0] = "world";
//            hd.setFilePath("qrwrwetp43");
//            hd.setFileTags(tags1);
//            elasticSearchQuery.createOrUpdateDocument(hd);
//            hd = new HeritageDocument();
//            String tags2[] = new String[3];
//            tags2[0] = "world";
//            tags2[1] = "bulgaria";
//            tags2[2] = "hungray";
//            hd.setFilePath("thjtyujqrwrwetp43");
//            hd.setFileTags(tags2);
        System.out.println("succcess");
        }


        catch(Exception e){
            System.out.println("Exception "+ e.toString());
        }
    }
}
