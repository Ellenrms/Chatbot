package com.ellenmateus.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ChatRequest {
    private String prompt;

    @JsonProperty("max_new_tokens")
    private int maxNewTokens;

    public ChatRequest() { }

    public ChatRequest(String prompt, int maxNewTokens) {
        this.prompt = prompt;
        this.maxNewTokens = maxNewTokens;
    }

    public String getPrompt() {
        return prompt;
    }
    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }

    public int getMaxNewTokens() {
        return maxNewTokens;
    }
    public void setMaxNewTokens(int maxNewTokens) {
        this.maxNewTokens = maxNewTokens;
    }
}
