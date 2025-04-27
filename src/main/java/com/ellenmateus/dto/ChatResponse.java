package com.ellenmateus.dto;

import java.util.List;

public class ChatResponse {
    private List<Result> results;

    public static class Result {
        private String text;
        public String getText() { return text; }
        public void setText(String text) { this.text = text; }
    }

    public ChatResponse(String botReply) {
		
	}
	public List<Result> getResults() { return results; }
    public void setResults(List<Result> results) { this.results = results; }
}
