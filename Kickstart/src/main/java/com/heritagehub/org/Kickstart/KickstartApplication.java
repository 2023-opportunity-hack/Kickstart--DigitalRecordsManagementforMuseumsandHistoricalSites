package com.heritagehub.org.Kickstart;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;

@SpringBootApplication
@EnableKafka
public class KickstartApplication {

	public static void main(String[] args) {
		SpringApplication.run(KickstartApplication.class, args);
	}

}
