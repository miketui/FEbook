import React, { useState } from 'react'
import { Sparkles, Brain, Wand2, AlertCircle, CheckCircle } from 'lucide-react'

const AIProcessor = ({ portfolioData, onAIResults }) => {
  const [isProcessing, setIsProcessing] = useState(false)
  const [aiResults, setAiResults] = useState(null)
  const [error, setError] = useState(null)
  const [processingProgress, setProcessingProgress] = useState(0)

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000'

  const processWithAI = async () => {
    setIsProcessing(true)
    setError(null)
    setProcessingProgress(0)

    try {
      // Prepare text inputs for AI processing
      const textInputs = []
      
      if (portfolioData.bio) {
        textInputs.push({
          content: `Name: ${portfolioData.name || 'Professional'}, Bio: ${portfolioData.bio}`,
          source: 'bio'
        })
      }

      if (portfolioData.name && portfolioData.title) {
        textInputs.push({
          content: `I'm ${portfolioData.name}, a ${portfolioData.title}`,
          source: 'profile'
        })
      }

      // Add contact and social information
      if (portfolioData.contact.location || portfolioData.contact.salon) {
        const locationInfo = []
        if (portfolioData.contact.location) locationInfo.push(`Location: ${portfolioData.contact.location}`)
        if (portfolioData.contact.salon) locationInfo.push(`Works at: ${portfolioData.contact.salon}`)
        
        textInputs.push({
          content: locationInfo.join(', '),
          source: 'contact'
        })
      }

      if (textInputs.length === 0) {
        throw new Error('Please provide some information about yourself first')
      }

      setProcessingProgress(20)

      // Make API call to AI backend
      const response = await fetch(`${API_BASE}/process-sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text_inputs: textInputs,
          profession_hint: detectProfession(),
          template_preference: 'modern'
        })
      })

      setProcessingProgress(60)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'AI processing failed')
      }

      const result = await response.json()
      
      setProcessingProgress(90)

      if (result.success) {
        setAiResults(result)
        onAIResults(result)
        setProcessingProgress(100)
      } else {
        throw new Error('AI processing completed but returned no results')
      }

    } catch (err) {
      console.error('AI processing error:', err)
      setError(err.message)
    } finally {
      setIsProcessing(false)
      setTimeout(() => setProcessingProgress(0), 2000)
    }
  }

  const detectProfession = () => {
    const text = `${portfolioData.title || ''} ${portfolioData.bio || ''}`.toLowerCase()
    
    const professionKeywords = {
      'hairstylist': ['hair', 'salon', 'cut', 'color', 'stylist', 'bridal hair'],
      'makeup_artist': ['makeup', 'mua', 'beauty', 'foundation', 'cosmetics'],
      'photographer': ['photo', 'camera', 'shoot', 'portrait', 'photography'],
      'fashion_stylist': ['fashion', 'styling', 'wardrobe', 'style consultant'],
      'nail_artist': ['nails', 'manicure', 'nail art', 'gel', 'acrylics'],
      'esthetician': ['skincare', 'facial', 'spa', 'aesthetics', 'skin care']
    }

    for (const [profession, keywords] of Object.entries(professionKeywords)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        return profession
      }
    }

    return 'hairstylist' // Default fallback
  }

  const enhanceWithAI = () => {
    if (!aiResults) return

    const profile = aiResults.professional_profile
    const content = aiResults.generated_content

    // Update portfolio data with AI enhancements
    const enhancedData = {
      ...portfolioData,
      name: profile.name || portfolioData.name,
      title: profile.profession ? profile.profession.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) : portfolioData.title,
      bio: content.bio || portfolioData.bio,
      aiEnhanced: true,
      aiGenerated: {
        services: content.services,
        about: content.about,
        specialties: profile.specialties || [],
        recommendations: aiResults.recommendations
      }
    }

    onAIResults(enhancedData)
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <Brain className="w-6 h-6 text-purple-500" />
        AI Portfolio Enhancement
      </h2>

      <div className="space-y-6">
        {/* AI Enhancement Description */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-4">
          <h3 className="font-semibold text-purple-900 mb-2 flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            AI-Powered Portfolio Analysis
          </h3>
          <p className="text-sm text-purple-800">
            Our AI analyzes your information and enhances your portfolio with professional content, 
            detects your profession, and provides personalized recommendations for templates and styling.
          </p>
        </div>

        {/* Processing Status */}
        {isProcessing && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Wand2 className="w-5 h-5 text-blue-600 animate-spin" />
              <span className="text-blue-900 font-medium">Processing with AI...</span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${processingProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-blue-700 mt-2">
              {processingProgress < 30 && "Analyzing your information..."}
              {processingProgress >= 30 && processingProgress < 70 && "Generating professional content..."}
              {processingProgress >= 70 && processingProgress < 100 && "Creating recommendations..."}
              {processingProgress === 100 && "Complete!"}
            </p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <span className="text-red-900 font-medium">AI Processing Error</span>
            </div>
            <p className="text-sm text-red-700 mt-1">{error}</p>
            <p className="text-xs text-red-600 mt-2">
              Make sure the AI backend is running and your API key is configured.
            </p>
          </div>
        )}

        {/* AI Results Display */}
        {aiResults && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-green-900 font-medium">AI Analysis Complete</span>
            </div>
            
            <div className="space-y-3">
              {aiResults.professional_profile.name && (
                <div>
                  <span className="text-sm font-medium text-green-800">Detected Name: </span>
                  <span className="text-sm text-green-700">{aiResults.professional_profile.name}</span>
                </div>
              )}

              {aiResults.professional_profile.profession && (
                <div>
                  <span className="text-sm font-medium text-green-800">Detected Profession: </span>
                  <span className="text-sm text-green-700">
                    {aiResults.professional_profile.profession.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                </div>
              )}

              {aiResults.professional_profile.specialties && aiResults.professional_profile.specialties.length > 0 && (
                <div>
                  <span className="text-sm font-medium text-green-800">Specialties: </span>
                  <span className="text-sm text-green-700">
                    {aiResults.professional_profile.specialties.join(', ')}
                  </span>
                </div>
              )}

              <div>
                <span className="text-sm font-medium text-green-800">Confidence Score: </span>
                <span className="text-sm text-green-700">
                  {Math.round(aiResults.confidence_score * 100)}%
                </span>
              </div>

              <div>
                <span className="text-sm font-medium text-green-800">Recommended Template: </span>
                <span className="text-sm text-green-700 capitalize">
                  {aiResults.recommendations.template}
                </span>
              </div>

              <div>
                <span className="text-sm font-medium text-green-800">Recommended Colors: </span>
                <span className="text-sm text-green-700 capitalize">
                  {aiResults.recommendations.color_scheme}
                </span>
              </div>
            </div>

            <button
              onClick={enhanceWithAI}
              className="mt-4 w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors duration-200"
            >
              Apply AI Enhancements
            </button>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={processWithAI}
            disabled={isProcessing}
            className="flex-1 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 transition-colors duration-200 flex items-center justify-center gap-2"
          >
            {isProcessing ? (
              <Wand2 className="w-5 h-5 animate-spin" />
            ) : (
              <Brain className="w-5 h-5" />
            )}
            {isProcessing ? 'Processing...' : 'Enhance with AI'}
          </button>
        </div>

        {/* Requirements */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">For best AI results:</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• Add your name and professional title</li>
            <li>• Write a detailed bio about your experience</li>
            <li>• Include your specialties and services</li>
            <li>• Mention your location and workplace</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default AIProcessor