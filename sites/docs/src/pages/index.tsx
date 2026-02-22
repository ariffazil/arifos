import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

import styles from './index.module.css';

export default function Home(): JSX.Element {
  return (
    <Layout
      title="arifOS"
      description="Constitutional intelligence kernel for governed AI systems."
    >
      <main>
        <section className={styles.hero}>
          <div className="container">
            <h1 className={styles.title}>arifOS</h1>
            <p className={styles.tagline}>
              Constitutional intelligence kernel that governs AI cognition via 13 floors and a
              000→999 metabolic pipeline.
            </p>
            <div className={styles.ctaRow}>
              <Link className="button button--primary button--lg" to="/intro">
                Read the docs
              </Link>
              <Link className="button button--secondary button--lg" to="/mcp-server">
                MCP server
              </Link>
              <Link className="button button--secondary button--lg" to="/governance">
                Governance
              </Link>
            </div>
          </div>
        </section>

        <section className={styles.grid}>
          <div className="container">
            <div className={styles.grid}>
              <div className={styles.card}>
                <h2>Operators</h2>
                <p>Run `aaa_mcp` in stdio/SSE/HTTP with floor enforcement and audit trails.</p>
              </div>
              <div className={styles.card}>
                <h2>Builders</h2>
                <p>Keep `core/` pure and `aaa_mcp/` transport-only. No layer mixing.</p>
              </div>
              <div className={styles.card}>
                <h2>Auditors</h2>
                <p>Understand floors F1–F13, SABAR_72, and 888_HOLD authority gating.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}

