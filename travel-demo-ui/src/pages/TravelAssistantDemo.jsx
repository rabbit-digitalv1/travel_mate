
import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";

export default function TravelAssistantDemo() {
  const [page, setPage] = useState(1);
  const [query, setQuery] = useState("");

  const handleNext = () => setPage((p) => p + 1);
  const handleBack = () => setPage((p) => p - 1);

  return (
    <div className="min-h-screen bg-white p-6 flex flex-col items-center justify-center space-y-8">
      <div className="max-w-xl w-full space-y-4">
        {page === 1 && (
          <Card>
            <CardContent className="p-6 space-y-4">
              <h1 className="text-2xl font-bold">🌍 Welcome to TravelQuery</h1>
              <p>
                Your personal travel assistant powered by AI. Discover places, plan routes,
                and get real-time travel insights.
              </p>
              <Button onClick={handleNext}>Start Exploring</Button>
            </CardContent>
          </Card>
        )}

        {page === 2 && (
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">🔍 Enter Your Travel Query</h2>
              <Input
                placeholder="e.g. Best hotels near Boudhanath for solo travelers"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <div className="flex justify-between">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
                <Button onClick={handleNext} disabled={!query}>
                  Search
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {page === 3 && (
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">✨ AI Recommendations</h2>
              <p className="text-sm text-gray-500">Query: {query}</p>
              <ul className="space-y-2">
                <li>🏨 Hotel Bodhi Tree — 4.5⭐, great hygiene, NPR 1800/night</li>
                <li>🛕 Close to Boudhanath Stupa (3 mins walk)</li>
                <li>🍽️ Recommended café: Himalayan Java nearby</li>
              </ul>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
                <Button onClick={handleNext}>View Route</Button>
              </div>
            </CardContent>
          </Card>
        )}

        {page === 4 && (
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">🗺 Suggested Route</h2>
              <p className="text-gray-600">Here's a custom route for your trip:</p>
              <ol className="list-decimal list-inside space-y-1">
                <li>Start at Tribhuvan Airport</li>
                <li>Head to Hotel Bodhi Tree</li>
                <li>Walk to Boudhanath Stupa</li>
                <li>Stop at Himalayan Java</li>
              </ol>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handleBack}>
                  Back
                </Button>
                <Button onClick={handleNext}>Save Trip</Button>
              </div>
            </CardContent>
          </Card>
        )}

        {page === 5 && (
          <Card>
            <CardContent className="p-6 space-y-4 text-center">
              <h2 className="text-xl font-bold">🎉 Trip Saved Successfully!</h2>
              <p>You can now access this route from your profile.</p>
              <Button onClick={() => setPage(1)}>Plan Another Trip</Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
