import React from 'react'
import { Link as LinkIcon, Instagram, Facebook, Youtube, Globe } from 'lucide-react'

const SocialLinks = ({ socialLinks, onSocialLinksChange }) => {
  const handleInputChange = (platform, value) => {
    onSocialLinksChange({
      ...socialLinks,
      [platform]: value
    })
  }

  const socialPlatforms = [
    {
      key: 'instagram',
      label: 'Instagram',
      icon: Instagram,
      placeholder: 'https://instagram.com/yourusername',
      color: 'bg-gradient-to-r from-purple-500 to-pink-500'
    },
    {
      key: 'facebook',
      label: 'Facebook',
      icon: Facebook,
      placeholder: 'https://facebook.com/yourpage',
      color: 'bg-blue-600'
    },
    {
      key: 'tiktok',
      label: 'TikTok',
      icon: () => (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
        </svg>
      ),
      placeholder: 'https://tiktok.com/@yourusername',
      color: 'bg-black'
    },
    {
      key: 'youtube',
      label: 'YouTube',
      icon: Youtube,
      placeholder: 'https://youtube.com/yourchannel',
      color: 'bg-red-600'
    },
    {
      key: 'website',
      label: 'Website',
      icon: Globe,
      placeholder: 'https://yourwebsite.com',
      color: 'bg-gray-600'
    }
  ]

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <LinkIcon className="w-6 h-6 text-primary-500" />
        Social Media & Links
      </h2>

      <div className="space-y-4">
        {socialPlatforms.map((platform) => {
          const IconComponent = platform.icon
          return (
            <div key={platform.key} className="flex items-center gap-4">
              <div className={`${platform.color} p-3 rounded-lg text-white flex-shrink-0`}>
                <IconComponent size={20} />
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {platform.label}
                </label>
                <input
                  type="url"
                  value={socialLinks[platform.key]}
                  onChange={(e) => handleInputChange(platform.key, e.target.value)}
                  placeholder={platform.placeholder}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                />
              </div>
            </div>
          )
        })}
      </div>

      <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
        <h3 className="font-semibold text-green-900 mb-2">🚀 Social Media Tips:</h3>
        <ul className="text-sm text-green-800 space-y-1">
          <li>• Include your most active social media profiles</li>
          <li>• Make sure your profiles are public and professional</li>
          <li>• Use consistent branding across all platforms</li>
          <li>• Regularly post your latest hair work</li>
          <li>• Engage with your followers and hair community</li>
        </ul>
      </div>
    </div>
  )
}

export default SocialLinks