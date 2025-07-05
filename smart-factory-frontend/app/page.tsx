'use client'

import { useState, useEffect } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ImageAnalysis } from '@/components/ImageAnalysis'
import { SensorMonitoring } from '@/components/SensorMonitoring'
import { Factory, Camera, Activity, Brain, Database, Cpu, Shield } from 'lucide-react'
import { ModelInsights } from '@/components/ModelInsights'

export default function Home() {
  const [currentTime, setCurrentTime] = useState<Date | null>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setCurrentTime(new Date())
    setIsVisible(true)
    const timer = setInterval(() => setCurrentTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const stats = [
    { icon: <Brain className="h-6 w-6" />, label: "AI Models", value: "2", desc: "CNN + LSTM" },
    { icon: <Database className="h-6 w-6" />, label: "Training Data", value: "50K+", desc: "Images & Sensors" },
    { icon: <Cpu className="h-6 w-6" />, label: "Accuracy", value: "98.2%", desc: "Production Ready" },
    { icon: <Shield className="h-6 w-6" />, label: "Deployment", value: "100%", desc: "Containerized" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-600/15 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl animate-pulse delay-500"></div>
        <div className="absolute top-1/3 right-1/3 w-80 h-80 bg-emerald-600/8 rounded-full blur-3xl animate-pulse delay-1500"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className={`text-center mb-12 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="relative">
              <Factory className="h-12 w-12 text-blue-400 animate-pulse" />
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-6xl md:text-7xl font-black text-white tracking-tight">
              Smart Factory
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-emerald-400">
                AI Platform
              </span>
            </h1>
          </div>
          
          <p className="text-xl md:text-2xl text-purple-100 max-w-4xl mx-auto mb-8 leading-relaxed">
            Advanced AI-powered quality control and anomaly detection system built with cutting-edge{' '}
            <span className="text-pink-300 font-semibold">computer vision</span> and{' '}
            <span className="text-emerald-300 font-semibold">deep learning</span> technologies
          </p>

          <div className="flex items-center justify-center gap-8 text-purple-200 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span>Live System</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span>{currentTime ? currentTime.toLocaleTimeString() : '--:--:--'}</span>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, index) => (
            <div 
              key={index}
              className={`bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-500 hover:scale-105 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
              style={{ transitionDelay: `${index * 100}ms` }}
            >
              <div className="flex items-center justify-center mb-3 text-purple-300">
                {stat.icon}
              </div>
              <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
              <div className="text-sm font-medium text-purple-200 mb-1">{stat.label}</div>
              <div className="text-xs text-purple-300/70">{stat.desc}</div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl p-8 mb-12">
          <Tabs defaultValue="image" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8 bg-white/10 border border-white/20">
              <TabsTrigger value="image" className="flex items-center gap-3 text-white data-[state=active]:bg-purple-500/20 data-[state=active]:text-purple-300">
                <Camera className="h-5 w-5" />
                Computer Vision AI
              </TabsTrigger>
              <TabsTrigger value="sensor" className="flex items-center gap-3 text-white data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-300">
                <Activity className="h-5 w-5" />
                Sensor Analytics
              </TabsTrigger>
            </TabsList>

            <TabsContent value="image">
              <Card className="bg-white/10 border-white/20 text-white">
                <CardHeader>
                  <CardTitle className="flex items-center gap-3 text-2xl">
                    <Camera className="h-6 w-6 text-purple-400" />
                    Advanced Computer Vision Quality Control
                  </CardTitle>
                  <CardDescription className="text-purple-200">
                    State-of-the-art CNN model trained on 50,000+ images for defect detection with 98.2% accuracy
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ImageAnalysis />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="sensor">
              <Card className="bg-white/10 border-white/20 text-white">
                <CardHeader>
                  <CardTitle className="flex items-center gap-3 text-2xl">
                    <Activity className="h-6 w-6 text-emerald-400" />
                    Real-time Sensor Anomaly Detection
                  </CardTitle>
                  <CardDescription className="text-emerald-200">
                    LSTM Autoencoder for predictive maintenance with 96.7% anomaly detection accuracy
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <SensorMonitoring />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Model Insights */}
        <ModelInsights />
      </div>
    </div>
  )
}

// Clock component for the time display
function Clock({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}
