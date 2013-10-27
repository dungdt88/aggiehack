<?php

namespace Visa\RouteFinderBundle\Route;

/**
 * Class Segment
 * @package Visa\RouteFinderBundle\Route
 */
class Segment
{
    /**
     * @var StopPoint
     */
    protected $start;
    
    /**
     * @var StopPoint
     */
    protected $end;
    
    /**
     * @var \DateTime
     */
    protected $time;
    
    /**
     * @var string
     */
    protected $type;

    /**
     * @var float
     */
    protected $duration;

    /**
     * @param StopPoint $start
     * @param StopPoint $end
     * @param \DateTime $time
     * @param string $type
     * @param float $duration
     */
    public function __construct(StopPoint $start, StopPoint $end, $time, $type, $duration)
    {
        $this->start = $start;
        $this->end = $end;
        $this->time = $time;
        $this->type = $type;
        $this->duration = $duration;
    }

    /**
     * @param \Visa\RouteFinderBundle\Route\StopPoint $end
     */
    public function setEnd($end)
    {
        $this->end = $end;
    }

    /**
     * @return \Visa\RouteFinderBundle\Route\StopPoint
     */
    public function getEnd()
    {
        return $this->end;
    }

    /**
     * @param \Visa\RouteFinderBundle\Route\StopPoint $start
     */
    public function setStart($start)
    {
        $this->start = $start;
    }

    /**
     * @return \Visa\RouteFinderBundle\Route\StopPoint
     */
    public function getStart()
    {
        return $this->start;
    }

    /**
     * @param \DateTime $time
     */
    public function setTime($time)
    {
        $this->time = $time;
    }

    /**
     * @return \DateTime
     */
    public function getTime()
    {
        return $this->time;
    }

    /**
     * @param string $type
     */
    public function setType($type)
    {
        $this->type = $type;
    }

    /**
     * @return string
     */
    public function getType()
    {
        return $this->type;
    }

    /**
     * @param float $duration
     */
    public function setDuration($duration)
    {
        $this->duration = $duration;
    }

    /**
     * @return float
     */
    public function getDuration()
    {
        return $this->duration;
    }
    
    
}