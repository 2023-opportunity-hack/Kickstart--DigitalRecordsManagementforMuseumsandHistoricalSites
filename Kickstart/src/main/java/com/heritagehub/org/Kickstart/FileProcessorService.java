package com.heritagehub.org.Kickstart;

import com.heritagehub.org.Kickstart.utilities.JsonUtil;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContentType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;

@Service
public class FileProcessorService {

    private final KafkaTemplate<String, FileMetadata> kafkaTemplate;
    private final RestHighLevelClient elasticsearchClient;

    @Autowired
    public FileProcessorService(KafkaTemplate<String, FileMetadata> kafkaTemplate,
                                RestHighLevelClient elasticsearchClient) {
        this.kafkaTemplate = kafkaTemplate;
        this.elasticsearchClient = elasticsearchClient;
    }

    public void processFilesInFolder(String folderPath) {
        File folder = new File(folderPath);
        File[] files = folder.listFiles();

        if (files != null) {
            for (File file : files) {
                // Process each file and gather metadata
                FileMetadata metadata = gatherFileMetadata(file);

                // Push metadata to Kafka topic
                kafkaTemplate.send("file-metadata-topic", metadata);
            }
        }
    }

    private FileMetadata gatherFileMetadata(File file) {
        // Implement your logic to gather file metadata
        // For example, you can get file name, size, date, etc.
        // and create a FileMetadata object
        FileMetadata metadata = new FileMetadata();
        metadata.setFilePath(file.getAbsolutePath());
        // Set other metadata fields

        return metadata;
    }

    @KafkaListener(topics = "file-metadata-topic", groupId = "file-consumer-group")
    public void consumeFileMetadata(FileMetadata metadata) {
        // Implement logic to create a document and push it to Elasticsearch
        // You can use the elasticsearchClient to interact with Elasticsearch
        try {
            IndexRequest indexRequest = new IndexRequest("your-index")
                    .source(JsonUtil.toJson(metadata), XContentType.JSON);
            IndexResponse response = elasticsearchClient.index(indexRequest, RequestOptions.DEFAULT);
            // Handle response if needed
        } catch (IOException e) {
            // Handle exception
        }
    }
}