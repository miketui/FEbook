import React from 'react'
import { Phone, Mail, MapPin, Building } from 'lucide-react'

const ContactInfo = ({ contact, onContactChange }) => {
  const handleInputChange = (field, value) => {
    onContactChange({
      ...contact,
      [field]: value
    })
  }

  const contactFields = [
    {
      key: 'email',
      label: 'Email Address',
      icon: Mail,
      type: 'email',
      placeholder: 'your.email@example.com',
      required: true
    },
    {
      key: 'phone',
      label: 'Phone Number',
      icon: Phone,
      type: 'tel',
      placeholder: '+1 (555) 123-4567',
      required: true
    },
    {
      key: 'location',
      label: 'Location/City',
      icon: MapPin,
      type: 'text',
      placeholder: 'City, State/Province',
      required: false
    },
    {
      key: 'salon',
      label: 'Salon/Studio Name',
      icon: Building,
      type: 'text',
      placeholder: 'Your Salon or Studio Name',
      required: false
    }
  ]

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <Phone className="w-6 h-6 text-primary-500" />
        Contact Information
      </h2>

      <div className="space-y-6">
        {contactFields.map((field) => {
          const IconComponent = field.icon
          return (
            <div key={field.key}>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                <IconComponent size={16} />
                {field.label}
                {field.required && <span className="text-red-500">*</span>}
              </label>
              <input
                type={field.type}
                value={contact[field.key]}
                onChange={(e) => handleInputChange(field.key, e.target.value)}
                placeholder={field.placeholder}
                required={field.required}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
              />
            </div>
          )
        })}

        {/* Booking Information */}
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h3 className="font-semibold text-purple-900 mb-3">📅 Booking Information</h3>
          <div className="space-y-3">
            <label className="flex items-center gap-2">
              <input type="checkbox" className="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-sm text-purple-800">Available for new clients</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" className="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-sm text-purple-800">Offer consultations</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" className="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-sm text-purple-800">Mobile/house call services</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" className="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-sm text-purple-800">Wedding/event services</span>
            </label>
          </div>
        </div>

        {/* Contact Tips */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h3 className="font-semibold text-amber-900 mb-2">💼 Professional Contact Tips:</h3>
          <ul className="text-sm text-amber-800 space-y-1">
            <li>• Use a professional email address</li>
            <li>• Include your business phone number</li>
            <li>• Make sure your location is accurate for local searches</li>
            <li>• Keep your contact information up to date</li>
            <li>• Consider adding your business hours</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default ContactInfo