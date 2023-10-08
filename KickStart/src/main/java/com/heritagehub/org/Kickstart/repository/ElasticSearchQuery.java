package com.heritagehub.org.Kickstart.repository;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.MatchQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.Query;
import co.elastic.clients.elasticsearch.core.*;
import co.elastic.clients.elasticsearch.core.search.Hit;
import com.heritagehub.org.Kickstart.models.HeritageDocument;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;
import org.springframework.util.StringUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;


@Repository
public class ElasticSearchQuery {

    @Autowired
    private ElasticsearchClient elasticsearchClient;

    private final String indexName = "heritagesprod";


    public String createOrUpdateDocument(HeritageDocument product) throws IOException {

        IndexResponse response = elasticsearchClient.index(i -> i
                .index(indexName)
                .id(product.getId())
                .document(product)
        );
        if(response.result().name().equals("Created")){
            return new StringBuilder("Document has been successfully created.").toString();
        }else if(response.result().name().equals("Updated")){
            return new StringBuilder("Document has been successfully updated.").toString();
        }
        return new StringBuilder("Error while performing the operation.").toString();
    }

    public HeritageDocument getDocumentById(String productId) throws IOException{
        HeritageDocument product = null;
        GetResponse<HeritageDocument> response = elasticsearchClient.get(g -> g
                        .index(indexName)
                        .id(productId),
                HeritageDocument.class
        );

        if (response.found()) {
            product = response.source();
            System.out.println("FIle Path " + product.getFilePath());
        } else {
            System.out.println ("Product not found");
        }

        return product;
    }

    public String deleteDocumentById(String productId) throws IOException {

        DeleteRequest request = DeleteRequest.of(d -> d.index(indexName).id(productId));

        DeleteResponse deleteResponse = elasticsearchClient.delete(request);
        if (Objects.nonNull(deleteResponse.result()) && !deleteResponse.result().name().equals("NotFound")) {
            return new StringBuilder("Product with id " + deleteResponse.id() + " has been deleted.").toString();
        }
        System.out.println("Product not found");
        return new StringBuilder("Product with id " + deleteResponse.id()+" does not exist.").toString();

    }

    public  List<HeritageDocument> searchAllDocuments() throws IOException {

        SearchRequest searchRequest =  SearchRequest.of(s -> s.index(indexName));
        SearchResponse searchResponse =  elasticsearchClient.search(searchRequest, HeritageDocument.class);
        List<Hit> hits = searchResponse.hits().hits();
        List<HeritageDocument> products = new ArrayList<>();
        for(Hit object : hits){

            System.out.print(((HeritageDocument) object.source()));
            products.add((HeritageDocument) object.source());

        }
        return products;
    }

    public List<HeritageDocument> searchByTagsWithWeightageAndPartialMatch(String userQuery) throws IOException {
        // Split the user query into words separated by spaces
        String[] userTags = userQuery.split("\\s+");

        // Create a list to store matching documents
        List<HeritageDocument> matchingDocuments = new ArrayList<>();
//
//        // Construct the Elasticsearch query JSON
//        String query = "{ \"query\": { \"bool\": { \"should\": [";
//
//        for (int i = 0; i < userTags.length; i++) {
//            // Construct the query for each tag word with boosting
//            String matchQuery = "{ \"match_phrase_prefix\": { \"tags\": { \"query\": \"" +
//                    userTags[i] + "\", \"boost\": " + (1.0 / (i + 1)) + " } } }";
//
//            query += matchQuery;
//
//            // Add a comma if it's not the last tag
//            if (i < userTags.length - 1) {
//                query += ", ";
//            }
//        }
//
//        query += "] } } }";
        Query fullNameQuery = MatchQuery.of(m -> m.field("tags").query(userTags[0]))._toQuery();
        SearchResponse<HeritageDocument> searchResponse = elasticsearchClient.search(s -> s.query(q -> q.bool(b -> b
                .should(fullNameQuery))
        ), HeritageDocument.class);

        for(Hit object : searchResponse.hits().hits()){

            System.out.print(((HeritageDocument) object.source()));
            matchingDocuments.add((HeritageDocument) object.source());

        }
        return matchingDocuments;
    }
}