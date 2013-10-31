<?php

namespace Csg\DataBundle\Service;

use Symfony\Component\Validator\Exception\InvalidArgumentException;

/**
 * Class GoogleDistanceClient
 * @package Csg\DataBundle\Service
 */
class GoogleDistanceClient
{
    /**
     * @var string
     */
    const MODE_WALKING = 'walking';
    
    /**
     * @var string
     */
    const MODE_DRIVING = 'driving';

    /**
     * @var string
     */
    const MODE_BICYCLING = 'bicycling';

    /**
     * @var string
     */
    private $baseApiUrl;

    /**
     * 
     */
    public function __construct()
    {
        $this->baseApiUrl = 'http://maps.googleapis.com/maps/api/distancematrix/';
    }

    /**
     * @param array $origins
     * @param array $destinations
     * @param string $mode
     * @return array
     * @throws \Symfony\Component\Validator\Exception\InvalidArgumentException
     */
    public function getDistanceMatrix(array $origins, 
                                      array $destinations, 
                                      $mode = self::MODE_WALKING)
    {
        // building querystring like this: ?origins=30.6056777003811,-96.3473367003999&destinations=30.6151660153369,-96.3520587296521|30.61190713,-96.318511&mode=walking&sensor=false

        if (!in_array($mode, array(self::MODE_BICYCLING, self::MODE_DRIVING, self::MODE_WALKING))) {
            throw new InvalidArgumentException('Invalid mode.');
        }

        $requestUrl = $this->baseApiUrl . '?';
        $queries = array();
        
        $originCoordinates = array();
        $destinationCoordinates = array();
        
        foreach ($origins as $origin) {
            if (2 === sizeof($origin)) {
                $originCoordinates[] = $origin[0] . ',' . $origin[1];
            }
        }

        $queries['origins'] = implode('|', $originCoordinates);

        foreach ($destinations as $destination) {
            if (2 === sizeof($destination)) {
                $destinationCoordinates[] = $destination[0] . ',' . $destination[1];
            }
        }
        
        $queries['destinations'] = implode('|', $destinationCoordinates);
        $queries['mode'] = $mode;
        $queries['sensor'] = 'false';
    
        
        $distanceMatrix = $this->googleApiCall($queries);
        
        return $distanceMatrix;
    }

    /**
     * @param array $queries
     * @return array
     */
    protected function googleApiCall(array $queries)
    {
        $requestUrl = $this->baseApiUrl . 'json?' . http_build_query($queries);

        $ch = curl_init();

        // set URL and other appropriate options
        curl_setopt($ch, CURLOPT_URL, $requestUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);

        // grab URL and pass it to the browser
        $response = trim(curl_exec($ch));

        // close cURL resource, and free up system resources
        curl_close($ch);
        
        return json_decode($response);
    }
}
