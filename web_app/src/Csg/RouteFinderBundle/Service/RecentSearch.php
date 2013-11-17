<?php

/**
 * 
 */

namespace Csg\RouteFinderBundle\Service;
use Symfony\Component\HttpFoundation\Session\Session;


/**
 * Class RecentSearch
 * @package Csg\RouteFinderBundle\Service
 */
class RecentSearch
{
    /**
     * 
     */
    
    const SS_KEY = 'recent_search_items';
    /**
     * @var \Symfony\Component\HttpFoundation\Session\Session
     */
    protected $session;
    /**
     * @var int
     */
    protected $maxItems;

    /**
     * Constructor
     *
     * @param \Symfony\Component\HttpFoundation\Session\Session $session
     * @param int $maxItems
     */
    public function __construct(Session $session, $maxItems = 5)
    {
        $this->session = $session;
        $this->maxItems = (int) $maxItems;
    }

    /**
     * Add new item to recent list
     * 
     * @param array $newRecentSearchItem
     * @return bool
     */
    public function add(array $newRecentSearchItem)
    {
        if (!isset($newRecentSearchItem['from_coordinate_lat']) || !isset($newRecentSearchItem['from_coordinate_long'])
            || !isset($newRecentSearchItem['to_coordinate_lat']) || !isset($newRecentSearchItem['to_coordinate_long'])
            || !isset($newRecentSearchItem['start_time'])) {
            return false;
        }

        $newRecentSearchItem['start_time'] = strtotime($newRecentSearchItem['start_time']);

        $recentSearchItems = $this->session->get(self::SS_KEY) ?: array();
        
        foreach ($recentSearchItems as $recentSearchItem) {
            if ($recentSearchItem['from_coordinate_lat'] == $newRecentSearchItem['from_coordinate_lat']
                && $recentSearchItem['from_coordinate_long'] == $newRecentSearchItem['from_coordinate_long']
                && $recentSearchItem['to_coordinate_lat'] == $newRecentSearchItem['to_coordinate_lat']
                && $recentSearchItem['to_coordinate_long'] == $newRecentSearchItem['to_coordinate_long']
                && $recentSearchItem['start_time'] == $newRecentSearchItem['start_time']) {
                return false;
            }
        }
        
        while ($this->maxItems <= sizeof($recentSearchItems)) {
            array_pop($recentSearchItems);
        }
        
        array_unshift($recentSearchItems, array(
            'from_coordinate_lat' => $newRecentSearchItem['from_coordinate_lat'],
            'from_coordinate_long' => $newRecentSearchItem['from_coordinate_long'],
            'to_coordinate_lat' => $newRecentSearchItem['to_coordinate_lat'],
            'to_coordinate_long' => $newRecentSearchItem['to_coordinate_long'],
            'start_time' => $newRecentSearchItem['start_time'],
            'from_name' => isset($newRecentSearchItem['from_name']) ? $newRecentSearchItem['from_name']
                    : $newRecentSearchItem['from_coordinate_lat'] . ', ' . $newRecentSearchItem['from_coordinate_long'],
            'to_name' => isset($newRecentSearchItem['to_name']) ? $newRecentSearchItem['to_name']
                : $newRecentSearchItem['to_coordinate_lat'] . ', ' . $newRecentSearchItem['to_coordinate_long'],
        ));
        
        $this->session->set(self::SS_KEY, $recentSearchItems);
        
        return true;
    }

    /**
     * @return array
     */
    public function getAll()
    {
        $recentSearch = $this->session->get(self::SS_KEY);
        
        return $recentSearch ?: array();
    }
}