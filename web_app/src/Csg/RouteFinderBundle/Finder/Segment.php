<?php

namespace Csg\RouteFinderBundle\Finder;

/**
 * Class Segment
 * @package Csg\RouteFinderBundle\Finder
 */
class Segment
{
    const TP_BUS = 'bus';
    const TP_WALK = 'walking';
    
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
     * @var string
     */
    protected $busNumber;

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
    public function __construct(StopPoint $start, StopPoint $end, \DateTime $time, $type, $duration)
    {
        $this->start = $start;
        $this->end = $end;
        $this->time = $time;
        
        if (self::TP_BUS === $type || self::TP_WALK === $type) {
            $this->type = $type;
        }
        
        $this->duration = $duration;
    }

    /**
     * @param \Csg\RouteFinderBundle\Finder\StopPoint $end
     * @return $this
     */
    public function setEnd($end)
    {
        $this->end = $end;

        return $this;
    }

    /**
     * @return \Csg\RouteFinderBundle\Finder\StopPoint
     */
    public function getEnd()
    {
        return $this->end;
    }

    /**
     * @param \Csg\RouteFinderBundle\Finder\StopPoint $start
     * @return $this
     */
    public function setStart($start)
    {
        $this->start = $start;

        return $this;
    }

    /**
     * @return \Csg\RouteFinderBundle\Finder\StopPoint
     */
    public function getStart()
    {
        return $this->start;
    }

    /**
     * @param \DateTime $time
     * @return $this
     */
    public function setTime($time)
    {
        $this->time = $time;

        return $this;
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
     * @return $this
     */
    public function setType($type)
    {
        $this->type = $type;

        return $this;
    }

    /**
     * @return string
     */
    public function getType()
    {
        return $this->type;
    }

    /**
     * @param string $busNumber
     */
    public function setBusNumber($busNumber)
    {
        $this->busNumber = $busNumber;
    }

    /**
     * @return string
     */
    public function getBusNumber()
    {
        return $this->busNumber;
    }

    /**
     * @return bool
     */
    public function isBus()
    {
        return self::TP_BUS === $this->type;
    }


    /**
     * @param float $duration
     * @return $this
     */
    public function setDuration($duration)
    {
        $this->duration = $duration;

        return $this;
    }

    /**
     * @return float
     */
    public function getDuration()
    {
        return $this->duration;
    }

    /**
     * @return string
     */
    public function getNiceDuration()
    {
        $duration = $this->getDuration();
        $niceDuration = '';
        $mapping = array(
            86400 => 'd',
            3600 => 'h',
            60 => 'm',
        );

        foreach ($mapping as $threshold => $text) {
            if ($duration >= $threshold) {
                $niceDuration .= (int) ($duration / $threshold) . "$text ";
                $duration = $duration % $threshold;
            }
        }

        if ($duration > 0) {
            $niceDuration .= $duration . 's';
        }

        return $niceDuration;
    }
}