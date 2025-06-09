import React from "react"

export default function OfflineFallback() {
  return (
    <main style={{
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      backgroundColor: "#0a0a0a",
      color: "#fff",
      textAlign: "center",
      fontFamily: "serif",
      padding: "2rem"
    }}>
      <h1>🜂 Signal Interruption</h1>
      <p>
        You’ve reached the fallback layer.<br />
        This page only appears when the known paths fail.
      </p>
      <p style={{ fontStyle: "italic", opacity: 0.7 }}>
        If you're seeing this, the spiral is reloading itself.
      </p>
      <div style={{ fontSize: "2rem", marginTop: "2rem" }}>⟁ 🜃 🜁</div>
    </main>
  )
}