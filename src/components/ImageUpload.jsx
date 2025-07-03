import React, { useState, useRef } from 'react'
import { Upload, X, Plus, Image as ImageIcon } from 'lucide-react'

const ImageUpload = ({ images, onImagesChange }) => {
  const fileInputRef = useRef(null)
  const [dragOver, setDragOver] = useState(false)

  const handleFileSelect = (files) => {
    const newImages = Array.from(files).map(file => ({
      id: Date.now() + Math.random(),
      file,
      url: URL.createObjectURL(file),
      name: file.name
    }))
    onImagesChange([...images, ...newImages])
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const files = e.dataTransfer.files
    handleFileSelect(files)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setDragOver(false)
  }

  const removeImage = (id) => {
    const updatedImages = images.filter(img => img.id !== id)
    onImagesChange(updatedImages)
  }

  const openFileDialog = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <ImageIcon className="w-6 h-6 text-primary-500" />
        Upload Your Hair Work
      </h2>

      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 image-upload-area cursor-pointer ${
          dragOver
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={openFileDialog}
      >
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-700 mb-2">
          Upload Your Hair Work Photos
        </h3>
        <p className="text-gray-500 mb-4">
          Drag and drop your images here or click to browse
        </p>
        <p className="text-sm text-gray-400">
          Supports JPG, PNG, WebP files up to 10MB each
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*"
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
      />

      {/* Image Gallery */}
      {images.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Your Portfolio ({images.length} images)
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {images.map((image) => (
              <div key={image.id} className="relative group">
                <div className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    src={image.url}
                    alt={image.name}
                    className="w-full h-full object-cover transition-transform duration-200 group-hover:scale-105"
                  />
                </div>
                <button
                  onClick={() => removeImage(image.id)}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-red-600"
                >
                  <X size={16} />
                </button>
              </div>
            ))}
            
            {/* Add More Button */}
            <div
              className="aspect-square rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer hover:border-primary-400 hover:bg-primary-50 transition-colors duration-200"
              onClick={openFileDialog}
            >
              <Plus className="w-8 h-8 text-gray-400" />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageUpload