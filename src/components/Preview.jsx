import React from 'react'
import { Download, Share2, Instagram, Facebook, Youtube, Globe, Mail, Phone, MapPin, Building } from 'lucide-react'

const Preview = ({ portfolioData }) => {
  const { images, bio, name, title, socialLinks, contact } = portfolioData

  const socialIcons = {
    instagram: Instagram,
    facebook: Facebook,
    youtube: Youtube,
    website: Globe,
    tiktok: () => (
      <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
        <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
      </svg>
    )
  }

  const exportPortfolio = () => {
    // This would implement export functionality
    alert('Export functionality would be implemented here!')
  }

  const sharePortfolio = () => {
    // This would implement share functionality
    alert('Share functionality would be implemented here!')
  }

  return (
    <div className="space-y-6">
      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 justify-center">
        <button
          onClick={exportPortfolio}
          className="flex items-center gap-2 bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 transition-colors duration-200"
        >
          <Download size={20} />
          Export Portfolio
        </button>
        <button
          onClick={sharePortfolio}
          className="flex items-center gap-2 bg-secondary-500 text-white px-6 py-3 rounded-lg hover:bg-secondary-600 transition-colors duration-200"
        >
          <Share2 size={20} />
          Share Portfolio
        </button>
      </div>

      {/* Portfolio Preview */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden max-w-4xl mx-auto">
        {/* Header Section */}
        <div className="bg-gradient-to-r from-primary-500 to-purple-600 text-white p-8 text-center">
          <h1 className="text-4xl font-bold mb-2">
            {name || 'Your Name'}
          </h1>
          <p className="text-xl opacity-90">
            {title || 'Professional Hair Stylist'}
          </p>
        </div>

        {/* Bio Section */}
        {bio && (
          <div className="p-8 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">About Me</h2>
            <p className="text-gray-700 leading-relaxed">
              {bio}
            </p>
          </div>
        )}

        {/* Portfolio Gallery */}
        {images.length > 0 && (
          <div className="p-8 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">My Work</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {images.map((image, index) => (
                <div key={image.id} className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    src={image.url}
                    alt={`Hair work ${index + 1}`}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Social Links */}
        <div className="p-8 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Follow My Work</h2>
          <div className="flex flex-wrap gap-4 justify-center">
            {Object.entries(socialLinks).map(([platform, url]) => {
              if (!url) return null
              const IconComponent = socialIcons[platform]
              if (!IconComponent) return null

              return (
                <a
                  key={platform}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg transition-colors duration-200"
                >
                  <IconComponent size={20} />
                  <span className="capitalize">{platform}</span>
                </a>
              )
            })}
          </div>
        </div>

        {/* Contact Information */}
        <div className="p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact Me</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {contact.email && (
              <div className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-primary-500" />
                <a href={`mailto:${contact.email}`} className="text-gray-700 hover:text-primary-500">
                  {contact.email}
                </a>
              </div>
            )}
            {contact.phone && (
              <div className="flex items-center gap-3">
                <Phone className="w-5 h-5 text-primary-500" />
                <a href={`tel:${contact.phone}`} className="text-gray-700 hover:text-primary-500">
                  {contact.phone}
                </a>
              </div>
            )}
            {contact.location && (
              <div className="flex items-center gap-3">
                <MapPin className="w-5 h-5 text-primary-500" />
                <span className="text-gray-700">{contact.location}</span>
              </div>
            )}
            {contact.salon && (
              <div className="flex items-center gap-3">
                <Building className="w-5 h-5 text-primary-500" />
                <span className="text-gray-700">{contact.salon}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Preview Note */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-4xl mx-auto">
        <h3 className="font-semibold text-blue-900 mb-2">🎨 Portfolio Preview</h3>
        <p className="text-sm text-blue-800">
          This is how your portfolio will appear to potential clients. You can export it as a webpage, 
          PDF, or share it directly on social media. Make sure all your information is complete before sharing!
        </p>
      </div>
    </div>
  )
}

export default Preview