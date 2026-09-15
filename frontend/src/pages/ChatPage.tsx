export function ChatPage() {
  return (
    <section className="panel chat-panel">
      <p className="eyebrow">Assistant</p>
      <h2>Chat</h2>
      <p className="lede">
        The agent, retrieval tools, streaming, and source citations are implemented in later
        phases. This is the conversation surface.
      </p>
      <div className="chat-thread" aria-label="Conversation placeholder">
        <article className="bubble assistant">
          Ask a question about your knowledge base. I will retrieve sources and cite them when
          the agent pipeline is live.
        </article>
      </div>
      <form className="composer" onSubmit={(event) => event.preventDefault()}>
        <input disabled placeholder="Chat is a placeholder until Phase 16" />
        <button type="submit" disabled>
          Send
        </button>
      </form>
    </section>
  );
}
