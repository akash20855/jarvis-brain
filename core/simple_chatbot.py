"""
Simple conversational chatbot for JARVIS fallback responses.
This provides quick responses for common user inquiries when AI backends are unavailable.
"""

class SimpleChatbot:
    """A simple rule-based chatbot for common conversational responses."""
    
    def __init__(self):
        """Initialize the chatbot with response mappings."""
        self.responses = {
            # Greetings
            "hi": "Hello! How can I assist you today?",
            "hy": "Hey! How's it going?",
            "hello": "Hi! What's on your mind?",
            "hey": "Hey there! What do you need?",
            "greetings": "Greetings! How can I help?",
            
            # Help requests
            "help": "I can help with various tasks! Ask me anything about JARVIS, coding, debugging, or just chat.",
            "what can you do": "I can help with code generation, debugging, chat, and more. Try asking me something!",
            "what is jarvis": "I'm JARVIS, your AI-powered development assistant integrated with VS Code.",
            
            # Exit commands
            "bye": "Goodbye! Feel free to reach out anytime.",
            "exit": "See you later!",
            "quit": "Catch you later!",
            
            # Status
            "how are you": "I'm functioning perfectly! Ready to help you.",
            "status": "All systems operational. How can I assist?",
            "are you there": "Yes, I'm here and ready to help!",
            
            # Calculator-related
            "calculator": "I can help with calculations! Just give me some numbers and an operation. What would you like to calculate?",
            "make a calculator": "Great! I'll create a calculator for you. What operations do you need? (add, subtract, multiply, divide)",
            "math": "I can help with math! Tell me what calculation you need.",
        }
    
    def respond(self, user_input):
        """
        Respond conversationally to user input.
        
        Args:
            user_input (str): The text entered by the user.
            
        Returns:
            str: A conversational response to the user's input, or None if no match found.
        """
        # Convert user input to lowercase for case-insensitive comparison
        normalized_input = user_input.lower().strip()
        
        # Check if the user input matches a key in the responses dictionary
        if normalized_input in self.responses:
            return self.responses[normalized_input]
        
        # Check for partial matches (contains key words)
        for key, response in self.responses.items():
            if key in normalized_input or normalized_input in key:
                return response
        
        # Return None if no match is found (caller will handle with AI backend)
        return None
    
    def add_response(self, user_input, response):
        """
        Add a custom response mapping.
        
        Args:
            user_input (str): The user input to match.
            response (str): The response to return.
        """
        self.responses[user_input.lower()] = response
    
    def get_all_responses(self):
        """
        Get all available responses.
        
        Returns:
            dict: All response mappings.
        """
        return self.responses.copy()


def main():
    """Interactive mode for testing the chatbot."""
    bot = SimpleChatbot()
    print("JARVIS Simple Chatbot (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot:", bot.respond(user_input))
            break
        
        response = bot.respond(user_input)
        if response:
            print(f"Bot: {response}")
        else:
            print("Bot: I'm not sure I understand. Can you please rephrase?")


if __name__ == "__main__":
    main()
