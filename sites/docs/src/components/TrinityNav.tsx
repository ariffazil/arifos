

export default function TrinityNav() {
  return (
    <nav className="trinity-nav">
      <div className="trinity-container">
        {/* Left: Logo + Trinity */}
        <div className="trinity-left">
          <a href="https://arif-fazil.com/" className="trinity-logo">
            <span className="arif">ARIF</span>
            <span className="os">OS</span>
          </a>
          <div className="trinity-badge">THE TRINITY</div>
        </div>

        {/* Center: The 3 Pillars */}
        <div className="trinity-center">
          <a href="https://arif-fazil.com/" className="trinity-link">HUMAN</a>
          <a href="https://apex.arif-fazil.com/" className="trinity-link">THEORY</a>
          <a href="https://arifos.arif-fazil.com/" className="trinity-link active">APPS</a>
        </div>

        {/* Right: Links */}
        <div className="trinity-right">
          <a href="https://github.com/ariffazil/arifOS" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          <a href="https://arif-fazil.com/" className="trinity-enter">
            Enter
          </a>
        </div>
      </div>
    </nav>
  );
}
