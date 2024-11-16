from volcenginesdkarkruntime import Ark


class DoubaoClient:
    def __init__(self):
        """
        Initialize the DoubaoClient with hardcoded API key and endpoint.
        """
        self.api_key = "fbcf73dd-657b-42da-afe4-70edd36bf553"
        self.model = "ep-20241116010811-gszj5"
        self.client = Ark(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=self.api_key)

    def chat(self, prompt):
        """
        Call the Doubao API chat endpoint.

        Args:
            prompt (str): The prompt to send to the Doubao model.

        Returns:
            str: The response from the Doubao model.
        """
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract habits and routines."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )

        response = ""  # Initialize an empty response string

        try:
            # If stream is iterable, parse each item in stream
            for chunk in stream:
                # Debug: Print the raw chunk for inspection
                print(f"DEBUG: Chunk received: {chunk}")

                # Parse the 'choices' part of the chunk
                if chunk[0] == "choices" and chunk[1]:
                    for choice in chunk[1]:
                        if hasattr(choice, "message") and choice.message.content:
                            response += choice.message.content
        except Exception as e:
            print(f"Error while processing stream: {e}")

        return response


if __name__ == "__main__":
    # 示例调用
    doubao_client = DoubaoClient()

    # 示例输入
    test_prompt = "What are the user's habits based on the provided schedule data?"
    try:
        response = doubao_client.chat(test_prompt)
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"Error during API call: {e}")