# Workflow: DESIGN
**Stage:** 400 (Design)  
**Band:** D (Design)  
**Purpose:** Create implementation-ready architecture blueprint  
**Trigger:** APPRAISE recommends proceeding  
**Output:** Design document ready for production handoff

---

## 🎯 When to Use

- **Architecture Definition**: "How exactly will we build this?"
- **Interface Design**: "What APIs and UIs do we need?"
- **Integration Planning**: "How does this fit with existing systems?"
- **Risk Mitigation**: "What could break and how do we prevent it?"
- **Roadmap Creation**: "What's the implementation sequence?"

**Key Signal**: We know WHAT to build; now we define HOW.

---

## 📋 Workflow Steps

### Step 1: Requirements Extraction (F2, F10)

**Constitutional Intent**: F2 Truth requires accurate requirements. F10 Ontology ensures proper categorization.

**Actions**:
1. **Extract from Appraisal**:
   - Functional requirements (what it does)
   - Non-functional requirements (how well it does it)
   - Constraints (time, budget, technology)

2. **Categorize Requirements**:
   - **MUST**: Critical for success
   - **SHOULD**: Important but not critical
   - **COULD**: Nice to have
   - **WON'T**: Explicitly out of scope

3. **Validate Completeness**:
   - Are all user needs covered?
   - Are integration points defined?
   - Are edge cases considered?

**Output**:
```yaml
requirements_spec:
  functional:
    - id: "FR-001"
      description: "System shall suggest code review comments"
      priority: "MUST"
      source: "S-001 (Code Reviewers)"
      acceptance_criteria: [...]
    - id: "FR-002"
      description: "System shall provide educational context"
      priority: "SHOULD"
      source: "S-002 (Junior Developers)"
      acceptance_criteria: [...]
    # ... more requirements
    
  non_functional:
    - id: "NFR-001"
      category: "performance"
      description: "Suggestions generated within 5 seconds"
      priority: "MUST"
      metric: "latency"
      target: "< 5s"
    - id: "NFR-002"
      category: "reliability"
      description: "99.9% uptime for suggestion API"
      priority: "SHOULD"
      metric: "availability"
      target: "99.9%"
    # ... more NFRs
    
  constraints:
    - type: "time"
      description: "Must ship within 2 weeks"
    - type: "budget"
      description: "OpenAI API costs < $100/month"
    - type: "technology"
      description: "Must use existing Python stack"
      
  traceability_matrix:
    FR-001: ["insight-I-001", "insight-I-002"]
    FR-002: ["insight-I-003"]
    # ... trace each requirement to discovery insights
```

---

### Step 2: Component Architecture (F8, F10)

**Constitutional Intent**: F8 Genius requires elegant design. F10 Ontology requires proper categorization.

**Actions**:
1. **Identify Components**: Major system parts
2. **Define Interfaces**: How components interact
3. **Map Dependencies**: What depends on what?
4. **Assign Responsibilities**: Single responsibility principle
5. **Technology Selection**: Choose appropriate tech for each

**Component Template**:
```yaml
component:
  id: "COMP-001"
  name: "SuggestionEngine"
  responsibility: "Generate code review suggestions"
  interfaces:
    - name: "generate_suggestions"
      input: "CodeDiff"
      output: "SuggestionList"
      protocol: "internal"
  dependencies: ["COMP-002", "COMP-003"]
  technology: "Python + OpenAI API"
  deployment: "Docker container"
```

**Output**:
```yaml
component_architecture:
  components:
    - id: "COMP-001"
      name: "GitHubWebhookHandler"
      responsibility: "Receive and validate GitHub webhooks"
      interfaces:
        - name: "handle_pull_request_event"
          input: "WebhookPayload"
          output: "ProcessedEvent"
      dependencies: []
      technology: "FastAPI"
      deployment: "Container"
      
    - id: "COMP-002"
      name: "DiffProcessor"
      responsibility: "Extract and chunk code diffs"
      interfaces:
        - name: "process_diff"
          input: "RawDiff"
          output: "ChunkedDiff"
      dependencies: []
      technology: "Python + tree-sitter"
      deployment: "Container"
      
    - id: "COMP-003"
      name: "EmbeddingService"
      responsibility: "Generate vector embeddings"
      interfaces:
        - name: "embed_chunks"
          input: "ChunkedDiff"
          output: "Embeddings"
      dependencies: []
      technology: "OpenAI API"
      deployment: "External service"
      
    - id: "COMP-004"
      name: "SuggestionEngine"
      responsibility: "Generate review suggestions"
      interfaces:
        - name: "generate_suggestions"
          input: "Embeddings + Context"
          output: "SuggestionList"
      dependencies: ["COMP-003"]
      technology: "Python + OpenAI API"
      deployment: "Container"
      
    - id: "COMP-005"
      name: "CommentPoster"
      responsibility: "Post suggestions to GitHub"
      interfaces:
        - name: "post_comments"
          input: "SuggestionList"
          output: "Success/Failure"
      dependencies: []
      technology: "PyGithub"
      deployment: "Container"
      
  architecture_diagram: |
    [GitHub] → [WebhookHandler] → [DiffProcessor]
                                      ↓
                              [EmbeddingService]
                                      ↓
                              [SuggestionEngine]
                                      ↓
                              [CommentPoster] → [GitHub]
  
  design_principles:
    - "Single Responsibility: Each component has one job"
    - "Loose Coupling: Components communicate via interfaces"
    - "High Cohesion: Related functionality grouped"
    - "Reversibility: Each component can be replaced"
```

---

### Step 3: Data Flow Design (F4, F8)

**Constitutional Intent**: F4 Clarity requires clean data flows. F8 Genius requires elegant data handling.

**Actions**:
1. **Map Data Flows**: How data moves through the system
2. **Define State Management**: Where is state stored?
3. **Plan Persistence**: What data is persisted and how?
4. **Design Transformations**: How is data transformed?

**Data Flow Example**:
```
Pull Request Event
    ↓
Webhook Handler (validation)
    ↓
Diff Processor (extraction)
    ↓
Chunked Diff (intermediate)
    ↓
Embedding Service (vectorization)
    ↓
Embeddings (cached)
    ↓
Suggestion Engine (generation)
    ↓
Suggestions (queued)
    ↓
Comment Poster (delivery)
    ↓
GitHub Comments
```

**Output**:
```yaml
data_flows:
  primary_flow:
    name: "Pull Request Review Flow"
    steps:
      - step: 1
        component: "GitHubWebhookHandler"
        input: "WebhookPayload"
        output: "ValidatedEvent"
        transformation: "Validate signature, parse payload"
        state_change: "None"
        
      - step: 2
        component: "DiffProcessor"
        input: "ValidatedEvent.diff_url"
        output: "ChunkedDiff[]"
        transformation: "Fetch diff, parse hunks, chunk by function"
        state_change: "Cache chunks in Redis (5 min TTL)"
        
      - step: 3
        component: "EmbeddingService"
        input: "ChunkedDiff[]"
        output: "Embedding[]"
        transformation: "Generate OpenAI embeddings"
        state_change: "Cache embeddings in Redis (1 hour TTL)"
        
      - step: 4
        component: "SuggestionEngine"
        input: "Embedding[] + Context"
        output: "Suggestion[]"
        transformation: "Generate suggestions via LLM"
        state_change: "Log suggestions to VAULT999"
        
      - step: 5
        component: "CommentPoster"
        input: "Suggestion[]"
        output: "PostedComment[]"
        transformation: "Format and post to GitHub"
        state_change: "Update PR with comments"
        
  state_management:
    cache:
      technology: "Redis"
      purpose: "Temporary storage for chunks/embeddings"
      ttl: "5 min - 1 hour"
    persistence:
      technology: "PostgreSQL"
      purpose: "Audit log, metrics, config"
    queue:
      technology: "Redis Queue"
      purpose: "Async processing of suggestions"
```

---

### Step 4: Interface Design (F6, F8)

**Constitutional Intent**: F6 Empathy requires user-centered design. F8 Genius requires elegant interfaces.

**Actions**:
1. **User Interface Design**: CLI, API, or Web UI
2. **API Specification**: REST/gRPC endpoints
3. **Error Handling**: How errors are communicated
4. **Accessibility**: Usability for weakest stakeholders

**Output**:
```yaml
interface_design:
  api_spec:
    endpoints:
      - path: "/webhook/github"
        method: "POST"
        description: "Receive GitHub webhook events"
        auth: "HMAC signature verification"
        request: "WebhookPayload"
        responses:
          200: "Accepted"
          400: "Invalid signature"
          500: "Processing error"
          
      - path: "/api/v1/suggestions"
        method: "GET"
        description: "Get suggestions for a PR"
        auth: "API key"
        parameters:
          - name: "pr_id"
            type: "string"
            required: true
        responses:
          200: "SuggestionList"
          404: "PR not found"
          
    schemas:
      Suggestion:
        type: "object"
        properties:
          id: {type: "string"}
          line_number: {type: "integer"}
          message: {type: "string"}
          severity: {type: "string", enum: ["info", "warning", "error"]}
          category: {type: "string"}
          confidence: {type: "number", minimum: 0, maximum: 1}
          
  cli_design:
    commands:
      - name: "review"
        description: "Review a pull request"
        args:
          - name: "pr-url"
            description: "URL of the PR to review"
        flags:
          - name: "--dry-run"
            description: "Generate suggestions without posting"
          - name: "--severity"
            description: "Minimum severity to report"
            default: "info"
            
  user_experience:
    weakest_stakeholder_focus: "S-002 (Junior Developers)"
    design_principles:
      - "Educational: Explain why, not just what"
      - "Constructive: Suggest improvements, don't just criticize"
      - "Clear: Use simple language, avoid jargon"
      - "Optional: Suggestions are advisory, not blocking"
    example_interaction: |
      AI Review: "Consider adding type hints here"
      
      Current code:
        def process(data):
      
      Suggested improvement:
        def process(data: dict) -> list:
      
      Why: Type hints help catch bugs early and improve IDE support.
      Learn more: [link to docs]
```

---

### Step 5: Risk Analysis (F5, F7)

**Constitutional Intent**: F5 Peace² requires risk mitigation. F7 Humility requires uncertainty acknowledgment.

**Actions**:
1. **Identify Risks**: Technical, operational, security
2. **Assess Impact**: What happens if risk occurs?
3. **Plan Mitigations**: How to prevent or reduce impact?
4. **Quantify Residual Risk**: What's left after mitigation?

**Risk Register**:
```yaml
risk:
  id: "R-001"
  category: "technical"
  description: "OpenAI API rate limits block processing"
  probability: 0.30
  impact: "high"
  risk_score: 0.30 × 0.8 = 0.24
  mitigation: "Implement exponential backoff, request limit increase"
  residual_probability: 0.10
  owner: "Engineering"
```

**Output**:
```yaml
risk_register:
  risks:
    - id: "R-001"
      category: "technical"
      description: "OpenAI API rate limits"
      probability: 0.30
      impact: "high"
      score: 0.24
      mitigation: "Exponential backoff, request limit increase"
      residual_probability: 0.10
      owner: "Engineering"
      
    - id: "R-002"
      category: "operational"
      description: "Service downtime prevents reviews"
      probability: 0.20
      impact: "medium"
      score: 0.12
      mitigation: "Health checks, auto-restart, monitoring alerts"
      residual_probability: 0.05
      owner: "DevOps"
      
    - id: "R-003"
      category: "security"
      description: "GitHub token compromised"
      probability: 0.10
      impact: "high"
      score: 0.08
      mitigation: "Token rotation, least privilege, secret scanning"
      residual_probability: 0.02
      owner: "Security"
      
    - id: "R-004"
      category: "adoption"
      description: "Team doesn't trust AI suggestions"
      probability: 0.40
      impact: "medium"
      score: 0.20
      mitigation: "Start with opt-in, demonstrate value, educational mode"
      residual_probability: 0.20
      owner: "Product"
      
  summary:
    total_risks: 4
    high_score_risks: ["R-001", "R-004"]
    residual_uncertainty: 0.04
    overall_risk_level: "MEDIUM"
```

---

### Step 6: Implementation Roadmap (F8)

**Constitutional Intent**: F8 Genius requires phased, achievable plan.

**Actions**:
1. **Define Phases**: Logical groupings of work
2. **Set Milestones**: Clear deliverables
3. **Estimate Timeline**: With uncertainty
4. **Define Success Criteria**: How we know each phase is done

**Output**:
```yaml
implementation_roadmap:
  phases:
    - id: "PHASE-1"
      name: "Foundation"
      duration: "Week 1"
      milestones:
        - name: "Project setup"
          deliverables: ["Repo created", "CI/CD pipeline", "Dev environment"]
          success_criteria: "Can deploy to staging"
        - name: "Webhook handler"
          deliverables: ["GitHub webhook endpoint", "Signature verification"]
          success_criteria: "Successfully receives PR events"
          
    - id: "PHASE-2"
      name: "Core Engine"
      duration: "Week 1-2"
      milestones:
        - name: "Diff processing"
          deliverables: ["Diff parser", "Code chunking"]
          success_criteria: "Correctly chunks 90% of PRs"
        - name: "Embedding pipeline"
          deliverables: ["OpenAI integration", "Embedding cache"]
          success_criteria: "Embeddings generated in < 2s"
          
    - id: "PHASE-3"
      name: "Suggestion Generation"
      duration: "Week 2"
      milestones:
        - name: "Suggestion engine"
          deliverables: ["LLM integration", "Prompt engineering"]
          success_criteria: "80% of suggestions are helpful"
        - name: "Comment posting"
          deliverables: ["GitHub comment API", "Formatting"]
          success_criteria: "Comments posted successfully"
          
    - id: "PHASE-4"
      name: "Deployment"
      duration: "Week 2"
      milestones:
        - name: "Production deploy"
          deliverables: ["Deployed to VPS", "Monitoring", "Documentation"]
          success_criteria: "Processing live PRs"
        - name: "Team onboarding"
          deliverables: ["Training session", "Usage guide"]
          success_criteria: "Team can use the tool"
          
  timeline:
    total_duration: "2 weeks"
    confidence: 0.80
    uncertainty_range: "1.5 - 3 weeks"
    
  dependencies:
    - "PHASE-2 depends on PHASE-1"
    - "PHASE-3 depends on PHASE-2"
    - "PHASE-4 depends on PHASE-3"
    
  rollback_plan: |
    If critical issues arise:
    1. Disable webhook in GitHub settings
    2. Revert to previous container image
    3. Notify team via Slack
    4. Post-mortem within 24 hours
```

---

## 📝 Output Specification

```yaml
design_package:
  metadata:
    workflow: "DESIGN"
    stage: "400"
    parent_appraisal: "session-id-from-appraise"
    session_id: "..."
    timestamp: "..."
    
  requirements_spec:
    functional: [...]
    non_functional: [...]
    constraints: [...]
    
  component_architecture:
    components: [...]
    architecture_diagram: "..."
    design_principles: [...]
    
  data_flows:
    primary_flow: {...}
    state_management: {...}
    
  interface_design:
    api_spec: {...}
    cli_design: {...}
    user_experience: {...}
    
  risk_register:
    risks: [...]
    summary: {...}
    
  implementation_roadmap:
    phases: [...]
    timeline: {...}
    rollback_plan: "..."
    
  constitutional_telemetry:
    floors_checked: ["F2", "F4", "F5", "F6", "F7", "F8", "F10"]
    design_principles_adhered: ["SRP", "Loose Coupling", "Reversibility"]
    
  verdict: "DESIGN_COMPLETE"
  recommendation: "PROCEED_TO_PRE_DEV_JUDGE"
```

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| **F2** | All design decisions trace to requirements | ✓ |
| **F4** | Architecture reduces complexity (clear components) | ✓ |
| **F5** | Risk register with mitigations | ✓ |
| **F6** | UX designed for weakest stakeholder | ✓ |
| **F7** | Timeline has uncertainty bounds | ✓ |
| **F8** | Components follow design principles | ✓ |
| **F10** | Proper categorization (MUST/SHOULD/COULD) | ✓ |

---

## 🔄 Next Stage

→ **Trigger**: `888-PRE-DEV-JUDGE`

---

**DITEMPA BUKAN DIBERI**
