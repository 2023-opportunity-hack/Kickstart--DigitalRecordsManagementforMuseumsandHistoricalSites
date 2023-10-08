package com.heritagehub.org.Kickstart.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;
import java.util.Date;

@Document(indexName = "heritagesprod")
public class HeritageDocument {

    @Id
    private String id;

    @Field(type = FieldType.Text, name = "filePath")
    private String filePath;

    @Field(type = FieldType.Text, name = "fileType")
    private String fileType;

    @Field(type = FieldType.Double, name = "price")
    private String[] tags;

    public String getFilePath() {
        return filePath;
    }

    public String getId() {
        return id;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public void setId(String id) {
        this.id=id;
    }

    public String [] getTags() {
        return tags;
    }

    public void setFileTags(String [] tags) {
        this.tags = tags;
    }
}