import React from 'react';
import { Github, ExternalLink, Database, Brain, LineChart } from 'lucide-react';

const HomePage = () => {
  const projects = [
    {
      title: "Data Analysis Pipeline",
      description: "Automated data processing and analysis pipeline for large-scale datasets",
      icon: <Database className="h-6 w-6" />,
    },
    {
      title: "ML Model Repository",
      description: "Collection of machine learning models for various prediction tasks",
      icon: <Brain className="h-6 w-6" />,
    },
    {
      title: "Interactive Visualizations",
      description: "Dynamic data visualizations for complex datasets",
      icon: <LineChart className="h-6 w-6" />,
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-blue-600 text-white">
        <div className="container mx-auto px-6 py-24">
          <h1 className="text-5xl font-bold mb-4">anDATA !bene</h1>
          <p className="text-xl mb-8">Transforming Data into Insights</p>
          <div className="flex gap-4">
            <button className="bg-white text-blue-600 px-6 py-2 rounded-lg flex items-center gap-2">
              <Github className="h-5 w-5" />
              View Projects
            </button>
            <button className="border border-white px-6 py-2 rounded-lg flex items-center gap-2">
              Contact Us
            </button>
          </div>
        </div>
      </div>

      {/* Projects Section */}
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold mb-12 text-center">Our Projects</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
              <div className="mb-4 text-blue-600">
                {project.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{project.title}</h3>
              <p className="text-gray-600 mb-4">{project.description}</p>
              <a href="#" className="text-blue-600 flex items-center gap-2 hover:underline">
                Learn more
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          ))}
        </div>
      </div>

      {/* About Section */}
      <div className="bg-gray-100">
        <div className="container mx-auto px-6 py-16">
          <h2 className="text-3xl font-bold mb-8 text-center">About Us</h2>
          <p className="text-gray-600 max-w-3xl mx-auto text-center">
            We are a passionate group of data scientists and analysts dedicated to solving complex problems through data-driven approaches. Our team combines expertise in machine learning, statistical analysis, and data visualization to deliver meaningful insights.
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white">
        <div className="container mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-xl font-bold">anDATA !bene</h3>
              <p className="text-gray-400">© 2025 All rights reserved</p>
            </div>
            <div className="flex gap-4">
              <Github className="h-6 w-6 cursor-pointer hover:text-blue-400" />
              <ExternalLink className="h-6 w-6 cursor-pointer hover:text-blue-400" />
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
