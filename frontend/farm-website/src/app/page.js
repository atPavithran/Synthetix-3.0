import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <h1 className="mb-5 text-farm-green text-3xl font-bold">Welcome to Farm Management</h1>
      <p className="text-lg leading-relaxed">
        Our platform helps you manage your agricultural operations efficiently. Track soil health, 
        monitor crop growth, and optimize your resources with our intelligent solutions.
      </p>
      
      <div className="mt-8">
        <h2 className="text-farm-green text-2xl font-semibold mb-4">Key Features</h2>
        <ul className="pl-5 space-y-3">
          <li className="text-base">Real-time monitoring of field conditions</li>
          <li className="text-base">Smart irrigation management</li>
          <li className="text-base">Crop health analytics</li>
          <li className="text-base">Weather forecasting and alerts</li>
          <li className="text-base">Resource optimization recommendations</li>
        </ul>
      </div>
      
      <div className="mt-8">
        <h2 className="text-farm-green text-2xl font-semibold mb-4">Getting Started</h2>
        <p className="text-base leading-relaxed">
          Navigate to the Dashboard to view your farm's current status and access detailed analytics.
          Our system uses advanced technology to provide you with actionable insights.
        </p>
      </div>
    </Layout>
  );
}