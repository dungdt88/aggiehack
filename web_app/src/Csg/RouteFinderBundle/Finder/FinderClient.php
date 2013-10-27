<?php
/**
 * 
 */

namespace Csg\RouteFinderBundle\Finder;

/**
 * Class FinderClient
 * @package Csg\RouteFinderBundle\Finder
 */
class FinderClient
{
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
        $_routes = $this->apiCall();
        $routes = array();

        foreach ($_routes as $_route) {
            $route = new Route();
            
            foreach ($_route as $_segment) {
                $_start = new StopPoint($_segment['start']['longitude'], $_segment['start']['latitude'], $_segment['start']['name']);
                $_end = new StopPoint($_segment['end']['longitude'], $_segment['end']['latitude'], $_segment['end']['name']);
                $_time = new \DateTime($_segment['time']);
                
                $segment = new Segment($_start, $_end, $_time, $_segment['type'], $_segment['duration']);
                $route->addSegment($segment);
            }
            
            $routes[] = $route;
        }
        
        return $routes;
    }

    /**
     * @return array
     */
    public function apiCall()
    {
        $routes = array();
        $types = array('bus', 'walk');
        
        for ($i = 0; $i < 3; $i ++) {
            $route = array();
            
            for ($j = 0; $j < 6; $j++) {
                $segment = array(
                    'start' => array(
                        'longitude' => 0.0,
                        'latitude' => 0.0,
                        'name' => '109 Maple ave College Station',
                    ),
                    'end' => array(
                        'longitude' => 0.0,
                        'latitude' => 0.0,
                        'name' => '109 Maple ave College Station',
                    ),
                    'time' => '2013-10-27 00:00:00',
                    'type' => $types[rand(0, 1)],
                    'duration' => 12345,
                );
                
                $route[] = $segment;
            }
            
            $routes[] = $route;
        }
        
        return $routes;
    }
}