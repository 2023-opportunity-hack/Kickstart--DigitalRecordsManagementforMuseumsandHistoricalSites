package com.heritagehub.org.Kickstart;

import com.heritagehub.org.Kickstart.repository.ElasticSearchQuery;
import com.heritagehub.org.Kickstart.service.FileProcessorService;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

import java.io.IOException;

@SpringBootApplication
@EnableAsync
public class KickstartApplication {

	@Autowired
	private static FileProcessorService fileProcessorService;

	public static void main(String[] args) throws IOException {
		SpringApplication.run(KickstartApplication.class, args);
		System.out.println("werguiwhepri");
	}



}
