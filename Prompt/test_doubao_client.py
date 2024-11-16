def test_chat_response():
    """
    Test the DoubaoClient's chat method with a hardcoded prompt.
    """
    from doubao_client import DoubaoClient

    # Initialize the client
    client = DoubaoClient()

    # Define the prompt for testing
    test_prompt = "Test habit extraction"

    try:
        # Call the chat method
        response = client.chat(test_prompt)
        print("DEBUG: Response from Doubao:", response)

        # Assertions
        assert response is not None, "Response should not be None"
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        print("Test passed: Valid response received.")
    except Exception as e:
        print(f"Test failed: {e}")