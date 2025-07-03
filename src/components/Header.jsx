import React from 'react'
import { Scissors, Sparkles } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-lg border-b border-gray-100">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-center">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Scissors className="w-8 h-8 text-primary-500" />
              <Sparkles className="w-4 h-4 text-yellow-400 absolute -top-1 -right-1" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
                Hair Portfolio Generator
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Create stunning portfolios to showcase your hair artistry
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header