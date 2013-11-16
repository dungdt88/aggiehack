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

//        localhost:5000/orgLat/30.61393756/orgLong/-96.33965217/desLat/30.62095300/desLong/-96.33822100/time/2013-11-07%2014:48:05.442433
        
        $requestPath = sprintf('/orgLat/%s/orgLong/%s/desLat/%s/desLong/%s/time/%s', 
            number_format($from->getLatitude(), 8), number_format($from->getLongitude(), 8),
            number_format($to->getLatitude(), 8), number_format($to->getLongitude(), 8), 
//            $startingTime->getTimestamp()
            strtotime('2013-11-07 14:48:05.442433')
        );
        
//        $requestPath = '/orgLat/30.61393756/orgLong/-96.33965217/desLat/30.62095300/desLong/-96.33822100/time/2013-11-07%2014:48:05.442433';
        
//        $response = $client->get($requestPath)->send();
//        
//        if (200 === $response->getStatusCode()) {
//            $responseObj = json_decode($response->getBody());
//            
//            if (!empty($responseObj->results)) {
//                foreach ($responseObj->results as $result) {
//                    $route = array();
//                    foreach ($result as $segment) {
//                        $route[] = array(
//                            'start' => array(
//                                'longitude' => $segment->start->long,
//                                'latitude' => $segment->start->lat,
//                                'name' => $segment->start->name,
//                            ),
//                            'end' => array(
//                                'longitude' => $segment->end->long,
//                                'latitude' => $segment->end->lat,
//                                'name' => $segment->end->name,
//                            ),
//                            'time' => strtotime($segment->start_time),
//                            'type' => $segment->type,
//                            'duration' => $segment->duration,
//                        );
//                    }
//                    
//                    $routes[] = $route;
//                }
//            } 
//        }
        
        $types = array('bus', 'walking');
        
        for ($i = 0; $i < 3; $i ++) {
            $route = array();
            
            for ($j = 0; $j < rand(2, 6); $j++) {
                $segment = array(
                    'start' => array(
                        'latitude' => 30.6215,
                        'longitude' => -96.3274,
                        'name' => 'Fish Pond',
                    ),
                    'end' => array(
                        'latitude' => 30.6206,
                        'longitude' => -96.3212,
                        'name' => 'Aggie Station',
                    ),
                    'time' => strtotime('2013-10-27 00:00:00'),
                    'type' => $types[rand(0, 1)],
                    'duration' => rand(50, 5000),
                );
                
                $route[] = $segment;
            }
            
            $routes[] = $route;
        }
        
        return $routes;
    }
}