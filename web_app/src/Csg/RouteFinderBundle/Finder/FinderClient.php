<?php
/**
 * 
 */

namespace Csg\RouteFinderBundle\Finder;

use Guzzle\Http\Client;

/**
 * Class FinderClient
 * @package Csg\RouteFinderBundle\Finder
 */
class FinderClient
{
    protected $apiUrl = 'http://localhost:5000';
    /**
     *
     */
    public function __construct()
    {
        
    }

    /**
     * @param StopPoint $from
     * @param StopPoint $to
     * @param \DateTime $startingTime
     * @return array
     */
    public function findRoutes(StopPoint $from, StopPoint $to, \DateTime $startingTime)
    {
        $_routes = $this->apiCall($from, $to, $startingTime);
        $routes = array();

        foreach ($_routes as $_route) {
            $route = new Route();
            
            foreach ($_route as $_segment) {
                $_start = new StopPoint($_segment['start']['longitude'], $_segment['start']['latitude'], $_segment['start']['name']);
                $_end = new StopPoint($_segment['end']['longitude'], $_segment['end']['latitude'], $_segment['end']['name']);
                $_time = new \DateTime(date('Y-m-d H:i:s', $_segment['time']));
//                $_time = new \DateTime('now');
                
                $segment = new Segment($_start, $_end, $_time, $_segment['type'], $_segment['duration']);
                $route->addSegment($segment);
            }
            
            $routes[] = $route;
        }
        
        return $routes;
    }

    /**
     * @param StopPoint $from
     * @param StopPoint $to
     * @param \DateTime $startingTime
     * @return array
     */
    public function apiCall(StopPoint $from, StopPoint $to, \DateTime $startingTime)
    {
        $routes = array();
        
        $client = new Client($this->apiUrl);
        $requestPath = sprintf('/lat1/%s/long1/%s/lat2/%s/long2/%s/time/%d', 
            $from->getLatitude(), $from->getLongitude(), 
            $to->getLatitude(), $to->getLongitude(), 
            $startingTime->getTimestamp());
        
        $response = $client->get($requestPath)->send();
        
        if (200 === $response->getStatusCode()) {
            $responseObj = json_decode($response->getBody());
            
            if (!empty($responseObj->results)) {
                foreach ($responseObj->results as $result) {
                    $route = array();
                    foreach ($result as $segment) {
                        $route[] = array(
                            'start' => array(
                                'longitude' => $segment->start->long,
                                'latitude' => $segment->start->lat,
                                'name' => $segment->start->name,
                            ),
                            'end' => array(
                                'longitude' => $segment->end->long,
                                'latitude' => $segment->end->lat,
                                'name' => $segment->end->name,
                            ),
                            'time' => strtotime($segment->start_time),
                            'type' => $segment->type,
                            'duration' => $segment->duration,
                        );
                    }
                    
                    $routes[] = $route;
                }
            } 
        }
        
//        $types = array('bus', 'walk');
//        
//        for ($i = 0; $i < 3; $i ++) {
//            $route = array();
//            
//            for ($j = 0; $j < 6; $j++) {
//                $segment = array(
//                    'start' => array(
//                        'longitude' => 0.0,
//                        'latitude' => 0.0,
//                        'name' => '109 Maple ave College Station',
//                    ),
//                    'end' => array(
//                        'longitude' => 0.0,
//                        'latitude' => 0.0,
//                        'name' => '109 Maple ave College Station',
//                    ),
//                    'time' => '2013-10-27 00:00:00',
//                    'type' => $types[rand(0, 1)],
//                    'duration' => 12345,
//                );
//                
//                $route[] = $segment;
//            }
//            
//            $routes[] = $route;
//        }
        
        return $routes;
    }
}