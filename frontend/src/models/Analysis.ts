import mongoose, { Schema, Document } from 'mongoose';

export interface IAnalysis extends Document {
  userId: string;
  resumeText: string;
  prediction: string;
  confidence: number;
  issues: string[];
  details: {
    skill_count: number;
    word_count: number;
    experience_years: number;
    skill_experience_ratio: number;
  };
  createdAt: Date;
}

const AnalysisSchema: Schema = new Schema({
  userId: { type: String, required: true },
  resumeText: { type: String, required: true },
  prediction: { type: String, required: true },
  confidence: { type: Number, required: true },
  issues: [{ type: String }],
  details: {
    skill_count: { type: Number },
    word_count: { type: Number },
    experience_years: { type: Number },
    skill_experience_ratio: { type: Number },
  },
  createdAt: { type: Date, default: Date.now },
});

export default mongoose.models.Analysis || mongoose.model<IAnalysis>('Analysis', AnalysisSchema);
