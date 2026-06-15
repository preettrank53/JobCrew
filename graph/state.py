from typing import TypedDict, Optional, Any, Dict, List
from pydantic import BaseModel, Field

class FitScore(BaseModel):
    overall_score: float = Field(..., description="Overall compatibility score from 0.0 to 10.0")
    dimension_breakdown: Dict[str, float] = Field(default_factory=dict, description="Breakdown per category like experience, skills, education")
    summary: str = Field(..., description="Summary explanation of the fit assessment")

class QualityScore(BaseModel):
    agent_name: str = Field(..., description="Name of the agent whose output was evaluated")
    score: float = Field(..., description="Quality score from 0.0 to 10.0")
    passed: bool = Field(..., description="Whether the output meets the quality threshold")
    feedback: str = Field("", description="Specific feedback on quality improvements")

class RAGMetadata(BaseModel):
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list, description="Raw document details retrieved")
    sources: List[str] = Field(default_factory=list, description="Unique source files or URLs used")
    collection_name: str = Field("", description="Name of the vector database collection queried")

class ExecutionMetadata(BaseModel):
    start_time: str = Field(..., description="Timestamp of when pipeline execution started")
    end_time: Optional[str] = Field(None, description="Timestamp of when pipeline execution ended")
    nodes_executed: List[str] = Field(default_factory=list, description="Sequence of graph nodes executed")
    provider_used: str = Field(..., description="Primary LLM provider used (e.g. Groq, Gemini)")
    errors: Dict[str, str] = Field(default_factory=dict, description="Dictionary mapping node names to error messages")

class JobCrewState(TypedDict):
    # User inputs
    candidate_profile: Dict[str, Any]
    job_description: str
    
    # Metadata
    job_source: str
    job_country: str
    
    # Analysis & Scoring
    job_analysis: Optional[str]
    fit_score: Optional[FitScore]
    
    # Pathing
    execution_path: Optional[str]
    execution_path_reason: Optional[str]
    
    # Agent Outputs
    resume_output: Optional[str]
    messaging_output: Optional[str]
    interview_prep_output: Optional[str]
    skills_gap_output: Optional[str]
    company_intel_output: Optional[str]
    
    # Trace & Quality metadata
    rag_metadata: Optional[Dict[str, RAGMetadata]]
    quality_scores: Optional[Dict[str, QualityScore]]
    execution_metadata: Optional[ExecutionMetadata]
    
    # Operational Status
    status: str
