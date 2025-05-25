package com.ellenmateus.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        // Usa SimpleClientHttpRequestFactory para não depender do Apache HttpClient
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);  // 5s para conectar
        factory.setReadTimeout(180000);    // 10s para ler resposta
        return new RestTemplate(factory);
    }
}
