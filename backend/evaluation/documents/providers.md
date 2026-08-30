# Language Model Providers

Nexus uses a provider abstraction for language models.

The provider interface separates the conversation service from the underlying
language model implementation.

Nexus currently supports Gemini as its language model provider.

The provider factory is responsible for creating the configured language model
provider.

The conversation service does not directly depend on the Gemini implementation.

This provider architecture makes it possible to replace the underlying
language model without changing the main conversation flow.

The language model provider exposes generation functionality for normal chat
responses.

Nexus also supports streaming responses through the provider architecture.