<?php
namespace Visa\RouteFinderBundle\Service;


/**
 * Class RouteFinder
 * @package Visa\RouteFinderBundle\Service
 */
/**
 * Class RouteFinder
 * @package Visa\RouteFinderBundle\Service
 */
class RouteFinder
{
    /**
     * @var string
     */
    protected $calculatorPath;
    
    /**
     *
     */
    public function __construct($calculatorPath)
    {
        $this->calculatorPath = $calculatorPath;
        $this->calculatorPath = realpath($this->calculatorPath);
    }

    /**
     * @param $fromLatitude
     * @param $fromLongitude
     * @param $toLatitude
     * @param $toLongitude
     * @param $startTime
     * @return array
     */
    public function findRoutes($fromLatitude, $fromLongitude, $toLatitude, $toLongitude, $startTime)
    {
        $startTime = date('H:i:s', strtotime($startTime));
        
        $handle = popen(sprintf('python %s', $this->calculatorPath . '/calculator.py'), 'r');
        $result = fread($handle, 100);
        $result = trim($result, " \n\r\t");

        $routes =$this->formatResult($result);
        
        $routes = array(
            array(
                'from' => '109 Maple ave College Station',
                'to' => 'Zachry Building',
                'time' => '20:00:00',
                'type' => 'Walk',
            ),
            array(
                'from' => '109 Maple ave College Station',
                'to' => 'Zachry Building',
                'time' => '20:00:00',
                'type' => 'Walk',
            ),
            array(
                'from' => '109 Maple ave College Station',
                'to' => 'Zachry Building',
                'time' => '20:00:00',
                'type' => 'Walk',
            ),
            array(
                'from' => '109 Maple ave College Station',
                'to' => 'Zachry Building',
                'time' => '20:00:00',
                'type' => 'Walk',
            ),
            array(
                'from' => '109 Maple ave College Station',
                'to' => 'Zachry Building',
                'time' => '20:00:00',
                'type' => 'Walk',
            ),
        );
        
        return $routes;
    }

    /**
     * @param $result
     * @return array
     */
    protected function formatResult($result)
    {
        return json_decode($result);
    }
}