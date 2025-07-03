import React from 'react'
import { User, Award, FileText } from 'lucide-react'

const BioSection = ({ bio, name, title, onBioChange, onNameChange, onTitleChange }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <User className="w-6 h-6 text-primary-500" />
        Profile & Bio
      </h2>

      <div className="space-y-6">
        {/* Name */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
            <User size={16} />
            Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => onNameChange(e.target.value)}
            placeholder="Enter your full name"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
          />
        </div>

        {/* Professional Title */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
            <Award size={16} />
            Professional Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => onTitleChange(e.target.value)}
            placeholder="e.g., Master Hair Stylist, Color Specialist, Salon Owner"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
          />
        </div>

        {/* Bio */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
            <FileText size={16} />
            Professional Bio
          </label>
          <textarea
            value={bio}
            onChange={(e) => onBioChange(e.target.value)}
            rows={6}
            placeholder="Tell your story... Share your experience, specialties, training, what makes you unique as a hair professional. This will help potential clients understand your expertise and approach."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 resize-none"
          />
          <div className="mt-2 text-sm text-gray-500">
            {bio.length}/500 characters
          </div>
        </div>

        {/* Tips */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">💡 Pro Tips for Your Bio:</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Mention your years of experience and specialties</li>
            <li>• Include any certifications or training</li>
            <li>• Highlight what makes your approach unique</li>
            <li>• Keep it personal but professional</li>
            <li>• Mention your favorite techniques or styles</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default BioSection