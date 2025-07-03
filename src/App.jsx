import React, { useState } from 'react'
import Header from './components/Header'
import ImageUpload from './components/ImageUpload'
import BioSection from './components/BioSection'
import SocialLinks from './components/SocialLinks'
import ContactInfo from './components/ContactInfo'
import Preview from './components/Preview'
import { User, Camera, Link, Phone, Eye } from 'lucide-react'

function App() {
  const [portfolioData, setPortfolioData] = useState({
    images: [],
    bio: '',
    name: '',
    title: '',
    socialLinks: {
      instagram: '',
      facebook: '',
      tiktok: '',
      youtube: '',
      website: ''
    },
    contact: {
      email: '',
      phone: '',
      location: '',
      salon: ''
    }
  })

  const [activeTab, setActiveTab] = useState('upload')

  const updatePortfolioData = (section, data) => {
    setPortfolioData(prev => ({
      ...prev,
      [section]: data
    }))
  }

  const tabs = [
    { id: 'upload', label: 'Upload Work', icon: Camera },
    { id: 'bio', label: 'Bio & Profile', icon: User },
    { id: 'social', label: 'Social Links', icon: Link },
    { id: 'contact', label: 'Contact Info', icon: Phone },
    { id: 'preview', label: 'Preview', icon: Eye }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        {/* Navigation Tabs */}
        <div className="flex flex-wrap justify-center mb-8">
          <div className="bg-white rounded-xl shadow-lg p-2 flex flex-wrap gap-2">
            {tabs.map((tab) => {
              const IconComponent = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-primary-500 text-white shadow-md'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <IconComponent size={18} />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Content Sections */}
        <div className="max-w-4xl mx-auto">
          {activeTab === 'upload' && (
            <ImageUpload 
              images={portfolioData.images}
              onImagesChange={(images) => updatePortfolioData('images', images)}
            />
          )}
          
          {activeTab === 'bio' && (
            <BioSection 
              bio={portfolioData.bio}
              name={portfolioData.name}
              title={portfolioData.title}
              onBioChange={(bio) => updatePortfolioData('bio', bio)}
              onNameChange={(name) => updatePortfolioData('name', name)}
              onTitleChange={(title) => updatePortfolioData('title', title)}
            />
          )}
          
          {activeTab === 'social' && (
            <SocialLinks 
              socialLinks={portfolioData.socialLinks}
              onSocialLinksChange={(links) => updatePortfolioData('socialLinks', links)}
            />
          )}
          
          {activeTab === 'contact' && (
            <ContactInfo 
              contact={portfolioData.contact}
              onContactChange={(contact) => updatePortfolioData('contact', contact)}
            />
          )}
          
          {activeTab === 'preview' && (
            <Preview portfolioData={portfolioData} />
          )}
        </div>
      </div>
    </div>
  )
}

export default App