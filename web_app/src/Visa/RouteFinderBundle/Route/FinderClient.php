<?php
/**
 * 
 */

namespace Visa\RouteFinderBundle\Route;

/**
 * Class FinderClient
 * @package Visa\RouteFinderBundle\Service
 */
/**
 * Class FinderClient
 * @package Visa\RouteFinderBundle\Route
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
        $routes = array();
        
        $segments = array();
        
        $start = new StopPoint(111, 222, '109 Maple ave College Station');
        $end = new StopPoint(111, 222, 'Zachry Building');
        $segments[] = new Segment($start, $end, new \DateTime('2013-10-22 00:00:00'), 'walk', 100);

        $start = new StopPoint(111, 222, '109 Maple ave College Station');
        $end = new StopPoint(111, 222, 'Zachry Building');
        $segments[] = new Segment($start, $end, new \DateTime('2013-10-22 00:00:00'), 'walk', 100);

        $start = new StopPoint(111, 222, '109 Maple ave College Station');
        $end = new StopPoint(111, 222, 'Zachry Building');
        $segments[] = new Segment($start, $end, new \DateTime('2013-10-22 00:00:00'), 'walk', 100);

        $start = new StopPoint(111, 222, '109 Maple ave College Station');
        $end = new StopPoint(111, 222, 'Zachry Building');
        $segments[] = new Segment($start, $end, new \DateTime('2013-10-22 00:00:00'), 'walk', 100);

        $start = new StopPoint(111, 222, '109 Maple ave College Station');
        $end = new StopPoint(111, 222, 'Zachry Building');
        $segments[] = new Segment($start, $end, new \DateTime('2013-10-22 00:00:00'), 'walk', 100);
        
        $routes[] = $segments;
        
        return $routes;
    }
}